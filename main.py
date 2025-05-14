import os
import subprocess
from pathlib import Path

import toml

from semver import Version
import semver

git_main_branch = os.getenv("GIT_TARGET_BRANCH", default = "main")
git_origin = os.getenv("GIT_ORIGIN", default = "origin")

version_file_name = "Cargo.toml"

subprocess.check_output([ "git", "fetch", git_origin, git_main_branch ])

# read old version file
old_version_file_content = subprocess.check_output(
    [ "git", "show", "{}/{}:{}".format(git_origin, git_main_branch, version_file_name)]
)

# read new version file
new_version_file_content = Path(version_file_name).read_text()

def get_version_from_file_content(content):
    content = toml.loads(content)
    version = content["version"]
    return Version.parse(version)

old_version = get_version_from_file_content(old_version_file_content)
new_version = get_version_from_file_content(new_version_file_content)

compare_result = semver.compare(old_version, new_version)
if compare_result >= 0:
    print("Error: incoming version must be greater than current version on {} branch\n", git_main_branch)
    print("       incoming_version = {}, current_version = {}", new_version, old_version)
    raise Exception("incoming version must be greater than current version")


if new_version.prerelease != None:
    print("Error: incoming version has prerelease part")
    raise Exception("incoming version has prerelease part")

if new_version.build != None:
    print("Error: incoming version has build part")
    raise Exception("incoming version has build part")
