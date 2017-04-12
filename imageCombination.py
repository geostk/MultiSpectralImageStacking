import cv2
import numpy as np
import arcpy
from arcpy.sa import *
from Tkinter import *
import tkFileDialog
import os

class App:


    def __init__(self, master):
        global frame
        frame = Frame(master)
        frame.pack()
        self.topBanner = Label(frame, text="Tyler Pubben's image processing GUI", font='bold').grid(row=0, column=0, columnspan=2)

        #Look for RGB files
        self.browseBtnRGB = Button(frame,
                             text = "Browse",
                             command=self.fileBrowseRGB, relief=RAISED, width=15).grid(row=1, column=1, padx=5)
        self.browseRGB = Label(frame, text="Select RGB Images to Load", width=30).grid(row=1, column=0, padx=5, pady=5)

        #look for normal files
        self.browseBtnNorms = Button(frame,
                                    text="Browse",
                                   command=self.fileBrowseNorms, relief=RAISED, width=15).grid(row=2, column=1, padx=5)
        self.browseNorms = Label(frame, text="Select Normal Images to Load", width=30).grid(row=2, column=0, padx=5, pady=5)

        # set output workspace
        self.wrkspaceBtn = Button(frame,
                                     text="Browse",
                                     command=self.workspaceSelect, relief=RAISED, width=15).grid(row=4, column=1, padx=5)
        self.browseWrkspace = Label(frame, text="Select output workspace", width=30).grid(row=4, column=0, padx=5, pady=5)


        # Run button


        self.runBtn = Button(frame, text = "RUN MULTISPECTRAL STACKING", fg="red", width = 30, relief=RAISED, command=self.mergeImages).grid(row=6,
                                                                            column=0, padx=10, pady=10, columnspan=2)

        # Classify images
        self.classifyIsoBtn = Button(frame, text="Run Isodata Classification", fg="blue", width=30, relief=RAISED,
                                     command=self.runIsoClassify).grid(
            row=8, column=0, columnspan=2, pady=5)



    def RGB_quantity(self):
        global frame
        global fileListRGB
        self.RGBCount = Label(frame, text = "Number of RGB files selected: "+str(len(fileListRGB))).grid(row=5, column=0)

    def Norm_quantity(self):
        global frame
        global fileListNorms
        self.NormCount = Label(frame, text="Number of normals files selected: " + str(len(fileListNorms))).grid(row=5,
                                                                                                         column=1)

    def workspaceSelect(self):
        global wrkspace
        wrkspace = tkFileDialog.askdirectory(parent=root, title='Choose Folder for exported files...')

    def fileBrowseRGB(self):
        global fileListRGB
        fileListRGB = tkFileDialog.askopenfilenames(parent=root, title='Choose RGB files to load...')
        self.RGB_quantity()

    def fileBrowseNorms(self):
        global fileListNorms
        fileListNorms = tkFileDialog.askopenfilenames(parent=root, title='Choose surface normal files to load...')
        self.Norm_quantity()

    def RGBimagesList(self):
        print "this is something"

    def mergeImages(self):  # This is where images are combined using ArcPy
        global fileListNorms
        global fileListRGB
        global wrkspace

        arcpy.env.workspace = wrkspace

        if len(fileListNorms) == len(fileListRGB):
            for RGBitem, NormItem in zip(fileListRGB, fileListNorms):
                fnamex = RGBitem.split('/')[-1].split('.')[0]+'_stacked.tif'
                arcpy.CompositeBands_management([RGBitem, NormItem], fnamex)

    def runIsoClassify(self):
        global wrkspace
        arcpy.env.workspace = wrkspace
        normalsList =  arcpy.ListRasters("*", "TIF")
        outDir = tkFileDialog.askdirectory(parent=root, title='Choose folder for output rasters.')
        print normalsList
        for raster in normalsList:
            outUnsupervised = IsoClusterUnsupervisedClassification (raster, 3)
            rasterOut = raster.split('.')[0]+"_classified.tif"
            outUnsupervised.save(os.path.join(outDir, rasterOut))


frame = None
fileListRGB = []
fileListNorms = []
wrkspace = None
root = Tk()
app = App(root)
root.wm_iconbitmap('im2.ico')
root.title('Multispectral Image Stacking Utility')
root.mainloop()