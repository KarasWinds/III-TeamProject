import os
import subprocess

def filerename(input_path):
    num = 1
    for path, dirs, files in os.walk(input_path):
        for f in files:
            file = path + f
            if os.path.isfile(file):
                print("S")
                os.rename(file, file.replace(file.split('.')[1].split('/')[-1],
                                             file.split('.')[1].split('/')[-2] + '-' + str(num)))
                num += 1

def renameall(input_path):
    filerename(input_path)
    for path, dirs, files in os.walk(input_path):
        for d in dirs:
            input_dir = path + d + '/'
            filerename(input_dir)

def converter(input_path, output_path):
    for path, dirs, files in os.walk(input_path):
        for d in dirs:
            outdir = output_path + "/" + d
            if not os.path.exists(outdir):
                os.mkdir(outdir)
        for f in files:
            inputfile = path + f
            if not os.path.isfile(inputfile):
                inputfile = path + "/" + f
            outputfile = inputfile.replace(input_path, output_path).replace(str(inputfile.split('.')[-1]), "mp3")
            cmdorder = "./ffmpeg/bin/ffmpeg -i " + inputfile + " -acodec libmp3lame " + outputfile
            subprocess.call(cmdorder, shell=False)
    print('success')
    return output_path

if __name__ == '__main__':
    # 將指定資料夾內(含子目錄下)全部檔案轉至MP3檔
    # 檔案名稱將重新命名為XXX-XX.mp3(序列化命名EX:type1-1)
    # ffmpeg程式資料夾需放置於python專案資料夾底下

    # 輸入資料夾位置
    input_path = './youtube/'
    # 輸出資料夾位置
    output_path = './audio_out/'

    if not os.path.exists(output_path):
        os.mkdir(output_path)
    # renameall(input_path)
    converter(input_path, output_path)