import subprocess

cmd = "git log --pretty=format:'%h|%ad|%s' --date=iso"
cmd = cmd.split(" ")

print("## Repository Changelog:\n")
res = subprocess.check_output(cmd)
for line in res.splitlines():
    line = line.decode("utf-8")
    if line.startswith("'") and line.endswith("'"):
        line = line[1:-1]
    line_parts = line.split("|")
    commit_hash = line_parts[0]
    commit_date = line_parts[1]
    commit_date = commit_date.replace(" +1300", "")
    commit_date = commit_date.replace(" +1200", "")
    print("#### %s: %s" % (commit_date, commit_hash))
    commit_msg = line_parts[2]
    commit_lines = commit_msg.split(". ")
    for msg in commit_lines:
        print("-", msg)
    print()
