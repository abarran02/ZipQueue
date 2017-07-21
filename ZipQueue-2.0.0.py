import os, shutil
while True:
    if not os.path.isfile('7za.exe'):
        input('7za.exe not found in working directory')
    else:
        break
from subprocess import call
from timeit import default_timer as timer
from time import sleep
from tkinter import *
from tkinter import messagebox

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.frame = Frame(master)
        self.frame.grid()

        self.queue = []
        self.namelist = []

        global acvar 
        acvar = IntVar(self)
        archive_button = Radiobutton(self.frame, text='Archive', variable=acvar, value=1, command=self.sel)
        archive_button.grid(row=1)
        extract_button = Radiobutton(self.frame, text='Extract', variable=acvar, value=2, command=self.sel)
        extract_button.grid(row=1, column=1)

        compress_label = Label(self.frame, text=' File(s) to queue ')
        compress_label.grid(row=2)
        self.compress = Entry(self.frame)
        self.compress.grid(row=2, column=1)

        add_button = Button(self.frame, text='Add to Queue', fg='blue', command=self.add)
        add_button.grid(row=4)
        start_button = Button(self.frame, text='Start Queue', fg='green', command=self.start)
        start_button.grid(row=4, column=1)

        output_label = Label(self.frame, text='Output path')
        output_label.grid(row=5)
        self.output = Entry(self.frame)
        self.output.grid(row=5, column=1)

        endaction_label = Label(self.frame, text='When finished')
        endaction_label.grid(row=6)
        endactions = ['Do nothing', 'Close ZipQueue', 'Shutdown']
        global eavar 
        eavar = StringVar(self)
        eavar.set(endactions[0])
        endaction = OptionMenu(self.frame, eavar, *endactions)
        endaction.grid(row=6, column=1)

    def sel(self):
        if acvar.get() == 1:
            self.archivename_label = Label(self.frame, text='Archive name')
            self.archivename_label.grid(row=3)
            self.archivename = Entry(self.frame)
            self.archivename.grid(row=3, column=1)
        else:
            try:
                self.archivename_label.destroy()
                self.archivename.destroy()
            except AttributeError:
                pass

    def add(self):
        files = self.compress.get()
        var = acvar.get()
        if var == 1:
            if os.path.isdir(files) or os.path.isfile(files):
                name = self.archivename.get()
                if name in self.namelist:
                    self.errbox('Archive name already in use')
                else:
                    self.compress.delete(first=0, last=len(files))
                    self.archivename.delete(first=0, last=len(name))
                    self.queue.append('7za a -t7z -mx9 "{0}" "{1}"'.format(name, files))
                    self.namelist.append(name)
            else:
                self.errbox('Enter a valid input path or filename')
        elif var == 2:
            if os.path.isfile(files):
                self.compress.delete(first=0, last=len(files))
                self.queue.append('7za x "%s"' % files)
            else:
                self.errbox('Enter a valid input filename')
        else:
            self.errbox('Select a 7-Zip action')

    def start(self):
        global output
        output = self.output.get()
        if not os.path.isdir(output):
            self.errbox('Enter a valid output path')
        else:
            try:
                shutil.copy2('7za.exe', output)
                os.chdir(output)
                self.runqueue()
            except shutil.SameFileError:
                self.runqueue()
            except IOError:
                self.errbox('Unable to write files to given output directory')

    def runqueue(self):
        start = timer()
        for action in self.queue:
            call(action)
        if not startwd == output:
            os.remove('7za.exe')
        end = eavar.get()
        if end == 'Do nothing':                
            self.queue = []
            os.chdir(startwd)
            messagebox.showinfo('Completed', '7-Zip queue completed in %s seconds' % round(timer() - start, 3))
        elif end == 'Shutdown':
            root.destroy()
            print('Shutting down in 60 seconds, close console window to abort')
            sleep(60)
            call('shutdown /s')
        else:
            quit()

    def errbox(self, message):
        messagebox.showerror('Error', message)

def gui():
    global root
    root = Tk()
    app = App(master=root)
    app.master.title('ZipQueue')
    app.master.resizable(width=False, height=False)
    app.mainloop()

if __name__ == '__main__':
    global startwd
    startwd = os.getcwd()
    gui()
