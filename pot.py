import sys
import os
import json
for_end=0
for_start=0
imp={} #imp模块导入格式:{"指令中文":"指令英文"}
#bate-v1.0.2
ver = "bate1.0.2"
tab = ""
class ModeVerErr(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
def chpyERR(e):
    print("----------------------")
    print("ERR:chpy运行报错!:")
    print(e)
    input("chpy编译器运行结束-回车退出")
    sys.exit(0)
chpyhelp = """
chpy编译器帮助信息:
    -build <源文件> <目标文件> [选项]:编译chpy程序
    -ver:查看chpy编译器版本
    -help:查看chpy编译器帮助信息
    -imp_info <模块目录/名字(注意是否有polist翻译文件,如果没有则会读取python自带模块信息)>:查看chpy编译器导入模块信息
"""
if len(sys.argv) < 2:
    print(chpyhelp)
    sys.exit(0)
if sys.argv[1]=="-build":
    if len(sys.argv) < 4:
        print("chpyBuild:缺少编译/构建重要参数!")
        print(chpyhelp)
        sys.exit(0)
    if ".py" in sys.argv[3]:
        out_file_name = sys.argv[3]
    else:
        out_file_name = sys.argv[3]+".py"
    print("正在编译程序:"+sys.argv[2])
    print("输出目标:"+sys.argv[2]+" -> "+out_file_name)
    if "-jump_err" in sys.argv:
        print("注意:跳过错误模式已开启,编译器将会在遇到错误时跳过该行并继续编译!")
    if "-run" in sys.argv:
        print("注意:运行模式已开启,编译器将会在编译完成后运行该程序!")
    f=open(sys.argv[2],"r",encoding="utf-8")
    fileline = f.readlines()
    f.close()
    with open(out_file_name,"w",encoding="utf-8") as f:
        f.write("")
        fls=""
        for line in fileline:
            command = line.split("|")
            command[0] = command[0].replace("\n", "")
            if command[0] == "pout" or command[0] == "输出":
                # bate-v1.0.2版本pout函数重构
                print("chpyBuild:写入-print函数")
                try:
                    fls=fls+tab+"print(\""+command[1].replace("\n", "").replace("-cr-", "")+"\"+str("+str(command[2]).replace("\n", "")+"))"+"\n"
                    print("chpyBuild:写入-调用变量>"+command[2].replace("\n", ""))
                except:
                    try:
                        fls=fls+tab+"print(\""+command[1].replace("\n", "")+"\")"+"\n"
                    except Exception as e:
                        chpyERR("ERR:错误的进入参数 "+ str(e))
            elif command[0] == "poin" or command[0] == "输入":
                print("chpyBuild:写入-input函数")
                try:
                    fls=fls+tab+command[2].replace("\n","")+" = input(\""+command[1]+"\")\n"
                except Exception as e:
                    chpyERR(e)
            elif command[0] == "import" or command[0] == "导入":
                print("chpyBuild:写入-导入模块")
                print("chpyBuild:写入-导入模块编译列表")
                try:
                    commls = command[1].split(".")
                    with open("./module/"+commls[0].replace("\n","")+".polist","r",encoding="utf-8") as imk:
                        imkline = imk.readline()
                        if ver in json.loads(imkline)["main_info"]["ver"]:
                            imp.update(json.loads(imkline))
                        else:
                            raise ModeVerErr("ERR:模块版本不匹配,请检查模块版本,模块版本:"+json.loads(imkline)["main_info"]["ver"]+" chpy编译器版本:"+ver)
                    fls=fls+tab+"import "+command[1].replace("\n","")+"\n"
                except Exception as e:
                    print(e)
                    print("ERR:导入模块错误,可能是模块编译列表不存在或者是模块版本不匹配")
                    if "-jump_err" in sys.argv:
                        print("chpyBuild:跳过错误")
                        fls=fls+tab+"# chpyBuild:跳过错误 错误:导入模块错误,可能是模块编译列表不存在或者是模块版本不匹配\n"
                    else:
                        chpyERR("ERR:导入模块错误,可能是模块编译列表不存在或者是模块版本不匹配")
            elif command[0] == "条件循环开始":
                print("chpyBuild:写入-条件循环开始")
                fls=fls+tab+"while "+command[1].replace("\n","")+":\n"
                tab = tab + "    "
            elif command[0] == "条件循环结束":
                print("chpyBuild:写入-条件循环结束")
                tab = tab[:-4]
            elif command[0] == "如果":
                print("chpyBuild:写入-条件判断")
                fls=fls+tab+"if "+command[1].replace("\n","")+":\n"
                tab = tab + "    "
            elif command[0] == "否则":
                print("chpyBuild:写入-条件判断-否则")
                tab = tab[:-4]
                fls=fls+tab+"else:\n"
                tab = tab + "    "
            elif command[0] == "条件判断结束":
                print("chpyBuild:写入-条件判断结束")
                tab = tab[:-4]
            elif command[0] == "新变量":
                print("chpyBuild:写入-新变量")
                fls=fls+tab+command[1].replace("\n","")+" = "+command[2].replace("\n","")+"\n"
            elif command[0] == "强制退出循环":
                print("chpyBuild:写入-强制退出循环")
                fls=fls+tab+"break\n"
                tab = tab[:-4]
            elif command[0] == "转数字":
                print("chpyBuild:写入-转数字")
                fls=fls+tab+command[1].replace("\n","")+"=int("+command[1].replace("\n","")+")\n"
            else:
                lsbool = False
                if command[0] in imp and command[0] != "main_info":
                    print("chpyBuild:写入-模块函数:"+command[0])
                    ls = "("
                    for i in range(len(command)):
                        if i == 0:
                            continue
                        else:
                            ls = ls + command[i].replace("\n", "") + ","
                            lsbool = True
                    if lsbool:
                        ls = ls[:-1]
                        lsbool = False
                    ls = ls + ")"
                    fls=fls+tab+imp[command[0]]+ls+"\n"
                else:
                    print("ERR:错误的指令!")
                    if "-jump_err" in sys.argv:
                        print("chpyBuild:跳过错误")
                        fls=fls+tab+"# chpyBuild:跳过错误 错误:错误的指令!\n"
                    else:
                        chpyERR("ERR:错误的指令!")
        if "-jump_err" in sys.argv:
            jump_err = True
        else:
            jump_err = False
        fls="# 文件名:"+out_file_name+"\n"+fls
        fls="# 是否跳过错误:"+str(jump_err)+"\n"+fls
        fls="# 该文件由chpy编译器编译\n"+fls
        print("chpyBuild:写入文件中...")
        f.write(fls)
        print("chpyBuild:写入完成!")
    try:
        if "-run" in sys.argv:
            print("chpyBuild:运行程序")
            os.system("python "+out_file_name)
    except:
        pass
elif sys.argv[1]=="-help":
    print(chpyhelp)
elif sys.argv[1]=="-ver":
    print("编译器版本:"+ver)
elif sys.argv[1]=="-imp_info":
    if len(sys.argv) < 3:
        print("ERR:缺少参数")
    else:
        print("chpyBuild:获取模块信息")
        try:
            with open(sys.argv[2],"r",encoding="utf-8") as f:
                fimk = f.readline()
                print("发现模块翻译文件")
                print("模块名称:"+json.loads(fimk)["main_info"]["name"])
                print("模块翻译文件作者备注:"+json.loads(fimk)["main_info"]["note"])
                print("模块翻译文件作者:"+json.loads(fimk)["main_info"]["by"])
                print("模块翻译文件支持编译器版本:")
                for i in json.loads(fimk)["main_info"]["ver"]:
                    print(i)
        except Exception as e:
            print(str(e))
            print("注意:没有找到模块翻译文件,下面是pip模块信息")
            os.system("pip show "+sys.argv[2])

else:
    print("ERR:错误的指令!")