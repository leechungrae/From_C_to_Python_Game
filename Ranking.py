from tkinter import *
#import PL_TeamProject

## 랭킹 시스템 미완성

def save_score():
        s_win = Tk()
        pyFrame = Frame(s_win, border=0)
        pyFrame.pack()
        pyFrame.master.title("이름 입력")

        pyLabel = Label(pyFrame, text="이름을 입력하세요.")
        pyLabel.pack()

        pyAttachFrame = Frame(pyFrame)
        pyText = Entry(pyAttachFrame)
        pyAttachFrame.pack(side="top")
        pyText.pack(side="top")
        pyBtn1 = Button(pyFrame, text="확인", command = save_data)
        pyBtn1.pack(side="left", padx=10, pady=10)
        pyBtn2 = Button(pyFrame, text="취소", command = s_win.destroy)
        pyBtn2.pack(side="right", padx=10, pady=10)

        s_win.mainloop()

def save_data():
            call_win = Tk()
            pyFrame = Frame(call_win, border = 50)
            pyFrame.pack()
            pyFrame.master.title("저장 완료")

            fileD = open('Ranking.txt','a')
            fileD.write("Name : ")
            fileD.write("abcd\t")
           # fileD.write(name+"\n")
            fileD.write("Score : ")
            fileD.write("90\n")
            fileD.close()

            pyLabel = Label(pyFrame, text="저장이 완료되었습니다.")
            pyLabel.pack(side="top")


            pyBtn1 = Button(pyFrame, text="순위 확인", command=show_ranking)
            pyBtn1.pack(side="left", padx=10, pady=10)

            pyBtn2 = Button(pyFrame, text="닫기", command=call_win.destroy)
            pyBtn2.pack(side="right", padx=10, pady=10)

            call_win.mainloop()


def show_ranking():
        rank_win = Tk()
        pyFrame = Frame(rank_win, border=50)
        pyFrame.pack()
        pyFrame.master.title("순위")
        pyAttachFrame = Frame(pyFrame)
        pyAttachFrame.pack(side="top")

        fileD = open('Ranking.txt', 'r')

        while True:
            fline = fileD.readline()
            if not fline: break
            pyLabel = Label(pyFrame, text=fline)
            pyLabel.pack()


        fileD.close()

        pyBtn1 = Button(pyFrame, text="확인", command=rank_win.destroy)
        pyBtn1.pack(side="bottom", padx=10, pady=10)
        rank_win.mainloop()


def main(score):
    root = Tk()
    pyFrame = Frame(root, border=50)
    pyFrame.pack()
    pyFrame.master.title("게임 종료")

    pyLabel = Label(pyFrame, text = "당신의 점수는 90점 입니다.\n 점수를 등록하시겠습니까?\n")
    pyLabel.pack()

    pyBtn = Button(pyFrame, text="예", command = save_score)
    pyBtn.pack(side = "left", padx=10, pady=10)
    pyBtn = Button(pyFrame, text="아니오", command = root.destroy)
    pyBtn.pack(side = "right", padx=10, pady=10)

    root.mainloop()

def gamescore(score):
    gscore = score

#if PL_TeamProject.Page == 3:
    a=3
    #game = create()
    #main(gscore)
#init()

