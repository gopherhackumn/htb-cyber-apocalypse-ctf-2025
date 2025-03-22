import json

with open("script.json", "rb") as f:
    data = json.loads(f.read())

sanitized = data["script"].replace("exec", "code = ")

exec(sanitized) # produces code variable

import dis

print(dis.code_info(code))

for insn in dis.get_instructions(code):
    print(insn)

