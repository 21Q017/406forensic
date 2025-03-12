import os
import sys
import subprocess

# 设置工具 JAR 包路径
APKTOOL_JAR = os.path.join(os.path.dirname(__file__), "apktool.jar")
APKSIGNER_JAR = os.path.join(os.path.dirname(__file__), "apksigner.jar")
print(r"""
    工具名称：ApkDebugerMaker apk自动添加允许调试功能工具
          _   _      ___     __     _____                                       _             
         | | | |    / _ \   / /_   |  ___|   ___    _ __    ___   _ __    ___  (_)   ___   ___ 
         | |_| |_  | | | | | '_ \  | |_     / _ \  | '__|  / _ \ | '_ \  / __| | |  / __| / __|
         |  _  _|  | |_| | | (_) | |  _|   | (_) | | |    |  __/ | | | | \__ \ | | | (__  \__ \
             |_|    \___/   \___/  |_|      \___/  |_|     \___| |_| |_| |___/ |_|  \___| |___/

            author: 金星路 406 取证人                                                                                 
    """)
# 显示帮助信息
def show_help():
    print("Usage: python script.py <apk_file>")
    print("\nThis script automatically decompiles an APK, modifies it to enable debugging, rebuilds, and signs it.")
    print("\nOptions:")
    print("  -h, --help    Show this help message and exit")
    sys.exit(0)

# 解析命令行参数
if len(sys.argv) != 2:
    show_help()

if sys.argv[1] in ['-h', '--help']:
    show_help()

apk_file = sys.argv[1]
apk_name = os.path.splitext(os.path.basename(apk_file))[0]
out_dir = f"{apk_name}_decompiled"
modified_apk = f"{apk_name}_modified.apk"
signed_apk = f"{apk_name}_signed.apk"

# 反编译 APK
def decompile_apk():
    cmd = ["java", "-jar", APKTOOL_JAR, "d", apk_file, "-o", out_dir, "--force-all"]
    if subprocess.run(cmd).returncode != 0:
        print("[Error] Failed to decompile APK")
        sys.exit(1)
    print("[Info] APK decompiled successfully.")

# 修改 AndroidManifest.xml 使应用可调试
def modify_manifest():
    manifest_file = os.path.join(out_dir, "AndroidManifest.xml")
    if not os.path.exists(manifest_file):
        print("[Error] AndroidManifest.xml not found!")
        sys.exit(1)
    
    with open(manifest_file, "r", encoding="utf-8") as file:
        content = file.read()
    
    if 'android:debuggable' in content:
        content = content.replace('android:debuggable="false"', 'android:debuggable="true"')
    else:
        content = content.replace("<application", "<application android:debuggable=\"true\"")
    
    with open(manifest_file, "w", encoding="utf-8") as file:
        file.write(content)
    print("[Info] AndroidManifest.xml modified to enable debugging.")

# 重新打包 APK
def rebuild_apk():
    cmd = ["java", "-jar", APKTOOL_JAR, "b", out_dir, "-o", modified_apk]
    if subprocess.run(cmd).returncode != 0:
        print("[Error] Failed to rebuild APK")
        sys.exit(1)
    print(f"[Info] APK rebuilt successfully: {modified_apk}")

# 签名 APK
def sign_apk():
    keystore_file = "keystore.jks"  # 确保密钥库文件存在
    alias_name = "mykey"
    keystore_pass = "password"
    key_pass = "password"
    
    cmd = [
        "java", "-jar", APKSIGNER_JAR, 
        "-keystore", keystore_file,
        "-alias", alias_name,
        "-pswd", keystore_pass,
        "-aliaspswd", key_pass,
        modified_apk
    ]
    
    if subprocess.run(cmd).returncode != 0:
        print("[Error] Failed to sign APK")
        sys.exit(1)
    print(f"[Info] APK signed successfully: {signed_apk}")
def main():
    decompile_apk()
    modify_manifest()
    rebuild_apk()
    sign_apk()
    print(f"[Success] Process completed! Signed APK: {signed_apk}")

if __name__ == "__main__":
   
    main()
