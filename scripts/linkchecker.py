#!/usr/bin/env python3
#
# This a link checker for Kubernetes documentation website.
# - We cover the following cases for the language you provide via `-l`, which
#   defaults to 'en'.
# - If the language specified is not English (`en`), we check if you are
#   actually using the localized links. For example, if you specify `zh` as
#   the language, and for link target `/docs/foo/bar`, we check if the English
#   version exists AND if the Chinese version exists as well. A checking record
#   is produced if the link can use the localized version.
#
# Usage: linkchecker.py -h
#
# Cases handled:
#
# - [foo](#bar)                         : ignored currently
# + [foo](http://bar)                   : insecure links to external site
# + [foo](https://k8s.io/website/...)   : hardcoded site domain name
#
# + [foo](/<lang>/docs/bar/...)  : where <lang> is not 'en'
#   + /<lang>/docs/bar           : contains shortcode, so ignore, or
#   + /<lang>/docs/bar           : is a image link (ignore currently), or
#   + /<lang>/docs/bar           : points to shared (non-localized) page, or
#   + /<lang>/docs/bar.md        : exists for current lang, or
#   + /<lang>/docs/bar/_index.md : exists for current lang, or
#   + /<lang>/docs/bar/          : is a redirect entry, or
#   + /<lang>/docs/bar           : is something we don't understand, then ERR
#
# + [foo](/docs/bar/...)
#   + /docs/bar                : contains shortcode, so ignore, or
#   + /docs/bar                : is a image link (ignore currently), or
#   + /docs/bar                : points to a shared (non-localized) page, or
#   + /docs/bar.md             : exists for current lang, or
#   + /docs/bar/_index.md      : exists for current lang, or
#   + /docs/bar                : is a redirect entry, or
#   + /docs/bar                : is something we don't understand
#
# + {{ < api-reference page="" anchor="" ... > }}
# + {{ < api-reference page="" > }}

import argparse
import glob
import os
import re
import sys

# These are the bad links that doesn't hurt, though good to fix
BAD_LINK_TYPES = {
    "B01": {
        "reason": "Using bad protocol",
        "level": "WARNING",
    },
    "B02": {
        "reason": "Link target is a redirect entry",
        "level": "WARNING",
    },
    "B03": {
        "reason": "Intra-site linkes should use relative path",
        "level": "WARNING",
    },
}

# Constants for colored printing
C_RED = "\033[31m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_GRAY  = "\033[90m"
C_CYAN = "\033[36m"
C_END = "\033[0m"

# Command line arguments shared across functions
ARGS = None
# Global result dictionary keyed by page examined
RESULT = {}
# Cached redirect entries
REDIRECTS = {}
# Cached anchors in target pages
ANCHORS = {}

def new_record(level, message, target):
    """Create new checking record.

    :param level: Record severity level, one of 'INFO', 'WARNING' and 'ERROR'
    :param message: Error message string
    :param target: The link target in question
    :returns: A string representation the checking result, may contain ASCII
              coded terminal colors, or None if the record is suppressed.
    """
    global ARGS

    # Skip info when verbose
    if ARGS.verbose == False and level == "INFO":
        return None

    result = None
    if ARGS.no_color:
        result = target + ": " + message
    else:
        target = C_GRAY + target + C_END
        if level == "INFO":
            result =  target + ": " + C_GREEN  + message + C_END 
        elif level == "WARNING":
            result = target + ": " + C_YELLOW+ message + C_END
        else:  # default to error
            result = target + ": " + C_RED + message + C_END

    return result


def dump_result():
    """Dump result to stdout."""
    global RESULT, ARGS

    for path, path_output in RESULT.items():
        norm_path = os.path.normpath(path)
        if ARGS.no_color:
            print("File: " + norm_path)
        else:
            print(C_CYAN + "File: " + norm_path + C_END)
        for p in path_output:
            print(" "*4 + p)
    return


def strip_comments(content):
    """Manual striping of comments from file content.

    Many localized content pages contain original English content in comments.
    These comments have to be stripped out before analyzing the links.
    Doing this using regular expression is difficult. Even the grep tool is
    not suitable for this use case.

    NOTE: We strived to preserve line numbers when producing the resulted
    text. This can be useful in future if we want to print out the line
    numbers for bad links.
    """
    result = []
    in_comment = False
    for line in content:
        idx1 = line.find("<!--")
        idx2 = line.find("-->")
        if not in_comment:
            # only care if new comment started
            if idx1 < 0:
                result.append(line)
                continue

            # single line comment
            if idx2 > 0:
                result.append(line[:idx1] + line[idx2+4:])
                continue
            result.append(line[:idx1])
            in_comment = True
            continue

        # already in comment block
        if idx2 < 0:  # ignore whole line
            result.append("")
            continue
        result.append(line[idx2+4:])
        in_comment = False

    return result


def normalize_filename(name, ftype="markdown"):
    """Guess the filename based on a link target.

    This function only deals with regular files.
    """
    if name.endswith("/"):
        name = name[:-1]
    if ftype == "markdown":
        name += ".md"
    else:
        name += ".html"
    return name


def check_file_exists(base, path, ftype="markdown"):
    """Check if the target file exists.

    NOTE: We build a normalized path using 'base' and 'path' values. Suppose
    the resulted path string is 'foo/bar', we check if 'foo/bar.md' exists,
    AND we check if 'foo/bar/_index.md' exists.

    :param base: The base directory to begin with
    :param path: The link target which is a relative path string
    :returns: A boolean indicating whether the target file exists.
    """
    # NOTE: anchor is ignored, can be a todo item
    parts = path.split("#")

    fn = normalize_filename(parts[0], ftype=ftype)
    target = base + fn

    if os.path.isfile(target):
        return True

    dir_name = base + parts[0]
    if os.path.isdir(dir_name):
        if os.path.isfile(dir_name + "/_index.md"):
            return True
        if os.path.isfile(dir_name + "/_index.html"):
            return True
        # /docs/contribute/style/hugo-shortcodes/ has this
        if os.path.isfile(dir_name + "/index.md"):
            return True
    return False


def get_redirect(path):
    """Check if the path exists in the redirect database.

    NOTE: We do NOT check if the redirect target is there or not. We do an
    **exact** matching for redirection entries.
    :returns: The redirect target if any, or None if not found.
    """
    global REDIRECTS

    def _check_redirect(t):
        for key, value in REDIRECTS.items():
            if key == t:  # EXACT MATCH
                return value
        return None

    # NOTE: anchor is ignored, can be a future todo
    parts = path.split("#")
    target = parts[0]
    if not target.endswith("/"):
        target += "/"

    new_target = _check_redirect(target)
    last_target = new_target
    while new_target:
        new_target = _check_redirect(new_target)
        if new_target is None:
            break
        last_target = new_target

    return last_target


def check_target(page, anchor, target):
    """Check a link from anchor to target on provided page.

    :param page: Currently not used. Passed here in case we want to check the
                 in-page links in the future.
    :param anchor: Anchor string from the content page. This is provided to
                help handle cases where target is empty.
    :param target: The link target string to check
    :returns: A checking record (string) if errors found, or None if we can
              find the target link.
    """
    target = target.strip()
    # B01: bad protocol
    if target.startswith("http://"):
        return new_record("WARNING", "Use HTTPS rather than HTTP", target)

    # full link
    if target.startswith("https://"):
        # B03: self link, should revise to relative path
        if (target.startswith("https://k8s.io/docs") or
                target.startswith("https://kubernetes.io/docs")):
            return new_record("ERROR", "Should use relative paths", target)
        # external link, skip
        return new_record("INFO", "External link, skipped", target)

    # in-page link
    # TODO: check if the target anchor does exists
    if target.startswith("#"):
        return new_record("INFO", "In-page link, skipped", target)

    # Link has shortcode
    if target.find("{{") > 0:
        return new_record("INFO", "Link has shortcode, skipped", target)

    # TODO: check links to examples
    if target.startswith("/examples/"):
        return new_record("WARNING", "Examples link, skipped", target)

    # it is an embedded image
    # TODO: an image might get translated as well
    if target.endswith(".png") or target.endswith(".svg"):
        return new_record("INFO", "Link to image, skipped", target)

    # link to English or localized page
    if (target.startswith("/docs/") or
            target.startswith("/" + ARGS.lang + "/docs/")):

        # target is shared reference (kubectl or kubernetes-api?
        if (target.find("/docs/reference/generated/kubectl/") >= 0 or
                target.find("/docs/reference/generated/kubernetes-api/") >= 0):
            if check_file_exists(ROOT + "/static", target, "html"):
                return None
            return new_record("ERROR", "Missing shared reference", target)

        # target is a markdown (.md) or a "<dir>/_index.md"?
        if target.startswith("/docs/"):
            base = os.path.join(ROOT, "content", "en")
        else:
            # localized target
            base = os.path.join(ROOT, "content")
        ok = check_file_exists(base, target)
        if ok:
            # We do't do additional checks for English site even if it has
            # links to a non-English page
            if ARGS.lang == "en":
                return None

            # If we are already checking localized link, fine
            if target.startswith("/" + ARGS.lang + "/docs/"):
                return None

            # additional check for localization even if English target exists
            base = os.path.join(ROOT, "content", ARGS.lang)
            found = check_file_exists(base, target)
            if not found:
                # Still to be translated
                return None
            msg = ("Localized page detected, please append '/%s' to the target"
                   % ARGS.lang)
            return new_record("ERROR", "Link not using localized page", target)

        # taget might be a redirect entry
        real_target = get_redirect(target)
        if real_target:
            msg = ("Link using redirect records, should use %s instead" %
                   real_target)
            return new_record("WARNING", msg, target)
        return new_record("ERROR", "Missing link for [%s]" % anchor, target)

    msg = "Link may be wrong for the anchor [%s]" % anchor
    return new_record("WARNING", msg, target)

def check_anchor(target_page, anchor):
    """Check if an anchor is defined in the target page

    :param target_page: The target page to check
    :param anchor: Anchor string to find in the target page
    """
    if target_page not in ANCHORS:
        try:
            with open(target_page, "r") as f:
                data = f.readlines()
        except Exception as ex:
            print("[Error] failed in reading markdown file: " + str(ex))
            return
        content = "\n".join(strip_comments(data))
        anchor_pattern1 = r"<a name=\"(.*?)\""
        regex1 = re.compile(anchor_pattern1)
        anchor_pattern2 = r"{#(.*?)}"
        regex2 = re.compile(anchor_pattern2)
        ANCHORS[target_page] = regex1.findall(content) + regex2.findall(content)
    return anchor in ANCHORS[target_page]

def check_apiref_target(target, anchor):
    """Check a link to an API reference page.

    :param target: The link target string to check
    :param anchor: Anchor string from the content page
    """
    base = os.path.join(ROOT, "content", "en", "docs", "reference", "kubernetes-api")
    ok = check_file_exists(base + "/", target)
    if not ok:
        return new_record("ERROR", "API reference page not found", target)

    if anchor is None:
        return

    target_page = os.path.join(base, target)+".md"
    if not check_anchor(target_page, anchor):
        return new_record("ERROR", "Anchor not found in API reference page", target+"#"+anchor)

def validate_links(page):
    """Find and validate links on a content page.

    The checking records are consolidated into the global variable RESULT.
    """
    try:
        with open(page, "r") as f:
            data = f.readlines()
    except Exception as ex:
        print("[Error] failed in reading markdown file: " + str(ex))
        return

    content = "\n".join(strip_comments(data))

    # Single results: searches for pattern: []()
    link_pattern = r"\[([`/\w\s\n]*)\]\(([^\)]*)\)"
    regex = re.compile(link_pattern)

    matches = regex.findall(content)
    records = []
    for m in matches:
        r = check_target(page, m[0], m[1])
        if r:
            records.append(r)

    # searches for pattern: {{< api-reference page="" anchor=""
    apiref_pattern = r"{{ *< *api-reference page=\"([^\"]*?)\" *anchor=\"(.*?)\""
    regex = re.compile(apiref_pattern)

    matches = regex.findall(content)
    for m in matches:
        r = check_apiref_target(m[0], m[1])
        if r:
            records.append(r)

    # searches for pattern: {{< api-reference page=""
    apiref_pattern = r"{{ *< *api-reference page=\"([^\"]*?)\""
    regex = re.compile(apiref_pattern)

    matches = regex.findall(content)
    for m in matches:
        r = check_apiref_target(m, None)
        if r:
            records.append(r)

    if len(records):
        RESULT[page] = records


def parse_arguments():
    """Argument parser.

    Result is returned and saved into global variable ARGS.
    """
    parser = argparse.ArgumentParser(description="Links checker for docs.")
    parser.add_argument("-l", dest="lang", default="en", metavar="<LANG>",
                        help=("two letter language code, e.g. 'zh'. "
                              "(default='en')"))
    parser.add_argument("-v", dest="verbose", action="store_true",
                        help="switch on verbose level")
    parser.add_argument("-f", dest="filter", default="/docs/**/*.md",
                        metavar="<FILTER>",
                        help=("File pattern to scan, e.g. '/docs/foo.md'. "
                              "(default='/docs/**/*.md')"))
    parser.add_argument("-n", "--no-color", action="store_true",
                        help="Suppress colored printing.")

    return parser.parse_args()


def main():
    """The main entry of the program."""
    global ARGS, ROOT, REDIRECTS

    ARGS = parse_arguments()
    print("Language: " + ARGS.lang)
    ROOT = os.path.join(os.path.dirname(__file__), '..')
    content_dir = os.path.join(ROOT, 'content')
    lang_dir = os.path.join(content_dir, ARGS.lang)

    # read redirects data
    redirects_fn = os.path.join(ROOT, "static", "_redirects")
    try:
        with open(redirects_fn, "r") as f:
            data = f.readlines()
        for item in data:
            parts = item.split()
            # There are entries without 301 specified
            if len(parts) < 2:
                continue
            entry = parts[0]
            # There are some entries not ended with "/"
            if entry.endswith("/"):
                REDIRECTS[entry] = parts[1]
            else:
                REDIRECTS[entry + "/"] = parts[1]

    except Exception as ex:
        print("[Error] failed in reading redirects file: " + str(ex))
        return

    folders = [f for f in glob.glob(lang_dir + ARGS.filter, recursive=True)]
    for page in folders:
        validate_links(page)

    dump_result()

    # Done
    print("Completed link validation.")


if __name__ == '__main__':
    sys.exit(main())
