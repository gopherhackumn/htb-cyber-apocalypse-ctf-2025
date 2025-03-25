# requires python-evtx and xmltodict
import base64

from Evtx.Evtx import Evtx
import xmltodict

s = "/Users/jeffreyhu/Documents/GitHub/htb-cyber-apocalypse-ctf-2025/forensics/cave_expedition/Logs/Microsoft-Windows-Sysmon_Operational.evtx"
# s = "/Users/jeffreyhu/Documents/GitHub/htb-cyber-apocalypse-ctf-2025/forensics/cave_expedition/Logs/Key Management Service.evtx"


with Evtx(s) as e:
    res = ""
    for r in e.records():
        x = r.xml()
        d = xmltodict.parse(x)
        # print(d["Event"]["EventData"]["Data"])
        if "powershell  -c" in str(d["Event"]["EventData"]["Data"]):
            s = d["Event"]["EventData"]["Data"][10]["#text"].split("\'")[1]
            res += s
    # print(res)
    print(base64.b64decode(res).decode())



# Interesting observations
"""
{'@Name': 'Image', '#text': 'C:\\Windows\\System32\\wevtutil.exe'}
{'@Name': 'Image', '#text': 'C:\\Windows\\System32\\cmd.exe'}
{'@Name': 'Image', '#text': 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'}
"""

"""
{'@Name': 'FileVersion', '#text': '10.0.19041.3996 (WinBuild.160101.0800)'}
{'@Name': 'TargetFilename', '#text': 'C:\\Users\\developer56546756\\AppData\\Local\\Temp\\__PSScriptPolicyTest_ijkwcd3l.pzc.ps1'}
{'@Name': 'FileVersion', '#text': '10.0.19041.3996 (WinBuild.160101.0800)'}
{'@Name': 'TargetFilename', '#text': 'C:\\Users\\developer56546756\\AppData\\Local\\Temp\\__PSScriptPolicyTest_pppqn3bn.s2v.ps1'}
{'@Name': 'FileVersion', '#text': '10.0.19041.3996 (WinBuild.160101.0800)'}
{'@Name': 'TargetFilename', '#text': 'C:\\Users\\developer56546756\\AppData\\Local\\Temp\\__PSScriptPolicyTest_z05dwe0b.o4i.ps1'}
{'@Name': 'FileVersion', '#text': '10.0.19041.3996 (WinBuild.160101.0800)'}
{'@Name': 'TargetFilename', '#text': 'C:\\Users\\developer56546756\\AppData\\Local\\Temp\\__PSScriptPolicyTest_hwnwstpn.ewr.ps1'}
{'@Name': 'FileVersion', '#text': '10.0.19041.3996 (WinBuild.160101.0800)'}
{'@Name': 'TargetFilename', '#text': 'C:\\Users\\developer56546756\\AppData\\Local\\Temp\\__PSScriptPolicyTest_fzpdckf3.rll.ps1'}
{'@Name': 'FileVersion', '#text': '10.0.19041.4355 (WinBuild.160101.0800)'}
{'@Name': 'TargetFilename', '#text': 'C:\\Users\\developer56546756\\Desktop\\avAFGrw41.ps1'}
{'@Name': 'FileVersion', '#text': '10.0.19041.3996 (WinBuild.160101.0800)'}
{'@Name': 'TargetFilename', '#text': 'C:\\Users\\developer56546756\\AppData\\Local\\Temp\\__PSScriptPolicyTest_xbr0mbzh.jkw.ps1'}
"""

"""
[{'@Name': 'RuleName', '#text': '-'}, {'@Name': 'UtcTime', '#text': '2025-01-28 10:31:17.554'}, {'@Name': 'ProcessGuid', '#text': '{9ef5b0ce-b1f5-6798-f804-000000001600}'}, {'@Name': 'ProcessId', '#text': '3152'}, {'@Name': 'Image', '#text': 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'}, {'@Name': 'FileVersion', '#text': '10.0.19041.3996 (WinBuild.160101.0800)'}, {'@Name': 'Description', '#text': 'Windows PowerShell'}, {'@Name': 'Product', '#text': 'Microsoft® Windows® Operating System'}, {'@Name': 'Company', '#text': 'Microsoft Corporation'}, {'@Name': 'OriginalFileName', '#text': 'PowerShell.EXE'}, {'@Name': 'CommandLine', '#text': 'powershell  -c "\'JGszNFZtID0gIktpNTBlSFFnS2k1a2IyTWdLaTVrYjJONElDb3VjR1JtIg0KJG03OFZvID0gIkxTMHRMUzB0TFMwdExTMHRMUzB0TFMwdExTMHRMUzB0TFMwdExTMHRMUzB0TFMwdExTMHRMUzB0TFMwdExTMHRMUzB0TFMwdExTMHRMUzB0TFMwdExTMHRMUzB0TFMwdExTMHRMUzB0TFMwdExTMHRMUzB0TFMwdExTMHRMUzB0TFFwWlQxVlNJRVpKVEVWVElFaEJWa1VnUWtWRlRpQkZUa05TV1ZCVVJVUWdRbGtnUVNCU1FVNVRUMDFYUVZKRkNpb2dWMmhoZENCb1lYQndaVzVsWkQ4S1RXOXpkQ0J2WmlCNWIzVnlJR1pwYkdWeklHRnlaU0J1YnlCc2IyNW5aWElnWVdOalpYTnphV0pzWlNCaVpXTmhkWE5sSUhSb1pYa2dhR0YyWlNCaVpXVnVJR1Z1WTNKNWNIUmxaQzRnUkc4Z2JtOTBJ\' | Out-File -Encoding ascii -FilePath b -NoNewline"'}, {'@Name': 'CurrentDirectory', '#text': 'C:\\Users\\developer56546756\\Desktop\\'}, {'@Name': 'User', '#text': 'WORKSTATION5678\\developer56546756'}, {'@Name': 'LogonGuid', '#text': '{9ef5b0ce-b10e-6798-e238-010000000000}'}, {'@Name': 'LogonId', '#text': '0x00000000000138e2'}, {'@Name': 'TerminalSessionId', '#text': '1'}, {'@Name': 'IntegrityLevel', '#text': 'High'}, {'@Name': 'Hashes', '#text': 'MD5=2E5A8590CF6848968FC23DE3FA1E25F1,SHA256=9785001B0DCF755EDDB8AF294A373C0B87B2498660F724E76C4D53F9C217C7A3,IMPHASH=3D08F4848535206D772DE145804FF4B6'}, {'@Name': 'ParentProcessGuid', '#text': '{9ef5b0ce-b1f5-6798-f704-000000001600}'}, {'@Name': 'ParentProcessId', '#text': '5364'}, {'@Name': 'ParentImage', '#text': 'C:\\Windows\\System32\\cmd.exe'}, {'@Name': 'ParentCommandLine', '#text': 'C:\\Windows\\system32\\cmd.exe /c ""C:\\Users\\developer56546756\\Desktop\\avAFGrw41.bat""'}, {'@Name': 'ParentUser', '#text': 'WORKSTATION5678\\developer56546756'}]
"""