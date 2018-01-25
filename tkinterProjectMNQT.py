from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from PIL import Image, ImageTk
from PIL import *
import cv2
import numpy as np

from Reflection import Reflection
from Rotation2 import Rotation2
from scale import Scale
from shear import Shear
from translate import Translate

class ProjectMNQT_UI:

    # cv2 images
    inputImage = None
    outputImage = None

    # file names
    outFileInitialName = ""
    currentOutFileName = ""

    # gui labels
    inputImageLabel = None
    outputImageLabel = None

    inputImageShapeLabel = None
    outputImageShapeLabel = None

    # gui entries
    rotationAngleEntry = None
    scaling_x_Entry = None
    scaling_y_Entry = None
    translation_x_Entry = None
    translation_y_Entry = None
    shear_m_Entry = None

    # gui pulldown
    interpVar = None
    reflectionVar = None
    shear_var = None

    maincanvas = None
    vsb = None
    mainframe = None

    # radio buttons
    transformationSelection = None

    # image sizes
    IMAGE_SIZE = (500, 500)

    def __init__(self, master): # master means root or main window

        master.configure(background="gainsboro")

        ## ****** Main Menu ******
        menu = Menu(master)

        master.config(menu=menu)
        subMenu = Menu(menu)

        menu.add_cascade(label="File", menu=subMenu)
        subMenu.add_command(label="Exit", command=quit)

        ## ****** Set Font ******
        myLargeFont = Font(family="Arial", size=24)
        mySmallFont = Font(family="Arial", size=16)

        ## ****** Top Toolbar ******
        toolbar = Frame(master, bg="slate gray")

        getImageButton = Button(toolbar, text="Get Image", command=self.getInputImage)
        getImageButton.pack(side=LEFT, padx=20, pady=20)

        projectNameLabel = Label(toolbar, text = "Image Geometric Transformation Project", font=myLargeFont, bg="slate gray")
        projectNameLabel.pack(side=LEFT, padx=100, pady=20)

        quitButton = Button(toolbar, text="Quit", command=quit)
        quitButton.pack(side=RIGHT, padx=20, pady=20)

        saveButton = Button(toolbar, text="Save Output Image", command=self.file_save)
        saveButton.pack(side=RIGHT, padx=20, pady=20)

        toolbar.pack(side=TOP, fill=X)

        ## ****** Status Bar ******
        self.statusLabel = Label(root, text="Started Project GUI", bd=1, relief=SUNKEN, anchor=W)
        self.statusLabel.pack(side=BOTTOM, fill=X)

        ## ****** Main Canvas  ******
        self.maincanvas = Canvas(root, borderwidth=0, background="gainsboro")
        self.vsb = Scrollbar(root, orient="vertical", command=self.maincanvas.yview)
        self.maincanvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.maincanvas.pack(side="left", fill="both", expand=True)


        ## ****** Main Window Frame ******
        self.mainframe = Frame(self.maincanvas, bg="gainsboro")  # frame is a blank widget
        #self.mainframe.pack()
        self.maincanvas.create_window((4,4), window=self.mainframe ,anchor="nw",
                                  tags="self.mainframe")
        self.mainframe.bind("<Configure>", self.onFrameConfigure)

        ## ****** Input image ******
        self.inputImageLabel = Label(self.mainframe)
        self.inputImageLabel.grid(row=0, column=0, columnspan=4, rowspan=4, sticky=W, padx=50, pady=30)


        ### ****** Transform Button ******
        transformButton = Button(self.mainframe, text="Transform", bd=0, highlightthickness=0, relief='ridge',
                                   command=self.runTransformation)
        transformButton.grid(row=0, column=4, columnspan=1, rowspan=4, sticky=W, padx=25, pady=25)

        buttonImage = cv2.imread("greenArrow.png")
        buttonImageDisplay = self.makeDisplayImage(buttonImage, (70, 70))
        transformButton.configure(image=buttonImageDisplay)
        transformButton.image = buttonImageDisplay


        ## ****** Output Image ******
        self.outputImageLabel = Label(self.mainframe)
        self.outputImageLabel.grid(row=0, column=5, columnspan=4, rowspan=4, sticky=E, padx=50, pady=30)


        ## ****** Put Empty Image in Image Labels ******
        empty_image = cv2.imread("empty_image.jpg")
        empty_image_display = self.makeDisplayImage(empty_image, self.IMAGE_SIZE)
        self.inputImageLabel.configure(image=empty_image_display)
        self.inputImageLabel.image = empty_image_display
        self.outputImageLabel.configure(image=empty_image_display)
        self.outputImageLabel.image = empty_image_display

        ## ****** Input image shape label ******
        self.inputImageShapeLabel = Label(self.mainframe, text="", bd=1, anchor=W, fg="red", bg="gainsboro")
        self.inputImageShapeLabel.grid(row=4, column=0, columnspan=2, rowspan=1, padx=50, pady=0)

        ## ****** Output image shape label ******
        self.outputImageShapeLabel = Label(self.mainframe, text="", bd=1, anchor=W, fg="red", bg="gainsboro")
        self.outputImageShapeLabel.grid(row=4, column=6, columnspan=2, rowspan=1, padx=50, pady=0)

        ## ****** Rotate Widget ******
        self.transformationSelection = IntVar()
        self.transformationSelection.set(0)
        rotationRadioButton = Radiobutton(self.mainframe, text="  Rotation (° counter clockwise)", font=mySmallFont, bg="gainsboro",
                                          variable=self.transformationSelection, value = 1)
        rotationRadioButton.grid(row=5, column=0, columnspan=2, rowspan=1, sticky=W, padx=50, pady=20)

        self.rotationAngleEntry = Entry(self.mainframe)
        self.rotationAngleEntry.grid(row=5, column=2, columnspan=1, rowspan=1, sticky=W)
        self.rotationAngleEntry.insert(0, '0')

        ## ****** Scaling Widget ******
        scalingRadioButton = Radiobutton(self.mainframe, text="  Scaling", font=mySmallFont, bg="gainsboro",
                                          variable=self.transformationSelection, value = 2)
        scalingRadioButton.grid(row=6, column=0, columnspan=1, rowspan=1, sticky=W, padx=50, pady=20)

        self.scaling_x_Entry = Entry(self.mainframe)
        self.scaling_x_Entry.grid(row=6, column=1, columnspan=1, rowspan=1, sticky=W)
        self.scaling_x_Entry.insert(0, 'Height')

        self.scaling_y_Entry = Entry(self.mainframe)
        self.scaling_y_Entry.grid(row=6, column=2, columnspan=1, rowspan=1, sticky=W)
        self.scaling_y_Entry.insert(0, 'Width')

        ## ****** Reflection Widget ******
        reflectionRadioButton = Radiobutton(self.mainframe, text="  Reflection", font=mySmallFont, bg="gainsboro",
                                          variable=self.transformationSelection, value = 3)
        reflectionRadioButton.grid(row=5, column=5, columnspan=1, rowspan=1, sticky=W, padx=0, pady=20)

        self.reflectionVar = StringVar(self.mainframe)
        self.reflectionVar.set("Reflection Type");

        reflectionPullDown = OptionMenu(self.mainframe, self.reflectionVar, "X-axis", "Y-axis")
        reflectionPullDown.grid(row=5, column=6, columnspan=2, rowspan=1, sticky=W, padx=0, pady=20)

        ## ****** Translation Widget ******
        translationRadioButton = Radiobutton(self.mainframe, text="  Translation", font=mySmallFont, bg="gainsboro",
                                         variable=self.transformationSelection, value=4)
        translationRadioButton.grid(row=6, column=5, columnspan=1, rowspan=1, sticky=W, padx=0, pady=20)

        self.translation_x_Entry = Entry(self.mainframe)
        self.translation_x_Entry.grid(row=6, column=6, columnspan=1, rowspan=1, sticky=W)
        self.translation_x_Entry.insert(0, 'x:px')

        self.translation_y_Entry = Entry(self.mainframe)
        self.translation_y_Entry.grid(row=6, column=7, columnspan=1, rowspan=1, sticky=W)
        self.translation_y_Entry.insert(0, 'y:px')

        ## ****** Shearing Widget ******
        shearRadioButton = Radiobutton(self.mainframe, text="  Shear", font=mySmallFont, bg="gainsboro",
                                          variable=self.transformationSelection, value = 5)
        shearRadioButton.grid(row=7, column=0, columnspan=1, rowspan=1, sticky=W, padx=50, pady=20)

        self.shear_m_Entry = Entry(self.mainframe)
        self.shear_m_Entry.grid(row=7, column=1, columnspan=1, rowspan=1, sticky=W)
        self.shear_m_Entry.insert(0, 'multiplier')

        self.shear_var = StringVar(self.mainframe)
        self.shear_var.set("Shear Type");

        shearPullDown = OptionMenu(self.mainframe, self.shear_var, "Horizontal", "Vertical")
        shearPullDown.grid(row=7, column=2, columnspan=2, rowspan=1, sticky=W, padx=0, pady=20)

        ## ****** Interpolation Pulldown ******
        interpolationLabel = Label(self.mainframe, text="        Interpolation:", bg="gainsboro", font=mySmallFont)
        interpolationLabel.grid(row=8, column=0, columnspan=2, rowspan=1, sticky=W, padx=50, pady=20)

        self.interpVar = StringVar(self.mainframe)
        self.interpVar.set("Interpolation");

        interpolationPullDown = OptionMenu(self.mainframe, self.interpVar, "Nearest_Neighbor", "Bilinear", "Bicubic")
        interpolationPullDown.grid(row=8, column=2, columnspan=2, rowspan=1, sticky=W, padx=0, pady=20)


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.maincanvas.configure(scrollregion=self.maincanvas.bbox("all"))

    def getInputImage(self):
        filename = filedialog.askopenfilename()
        if filename is None:
            self.setStatus("No input file chosen in filedialog.")
            return

        self.outFileInitialName = self.getInitialOutputFilename(filename)

        self.inputImage = cv2.imread(filename)
        self.inputImage = cv2.cvtColor(self.inputImage, cv2.COLOR_RGB2GRAY)

        self.displayImageOnLabel(self.inputImageLabel, self.inputImage, self.IMAGE_SIZE)

        image_shape = self.inputImage.shape
        image_shape_str = "Input Image Size: " + str(image_shape)
        self.inputImageShapeLabel.configure(text=image_shape_str)
        self.inputImageShapeLabel.text = image_shape_str

        self.setStatus("Loaded input image: " + filename)

    def getInitialOutputFilename(self, filenameWithPath):
        """ Return initial output file name """
        splitString = filenameWithPath.split("/")
        lastName = splitString[len(splitString) - 1]
        fileSplitString = lastName.split(".")
        fileString = fileSplitString[0]
        if fileString == "":
            fileString = "UnknownFile"
        fileString = fileString.replace(" ", "_")
        return fileString

    def file_save(self):
        self.currentOutFileName = self.currentOutFileName.replace(".", "p")
        #print(self.currentOutFileName)
        outFileName = filedialog.asksaveasfilename(title=("Save Output Image"), initialfile=self.currentOutFileName,
                                                   defaultextension=".png")
        if outFileName is None:
            self.setStatus("No save file chosen.")
            return

        cv2.imwrite(outFileName, self.outputImage)

    def runTransformation(self):
        if self.inputImage is None:
            self.setStatus("Please load and input image.")
            return

        if self.transformationSelection.get() == 1:
            # rotation
            rotationObject = Rotation2(self.inputImage, self.retrieveRotationAngle())

            rotationType = None
            rotated_image = None
            if self.interpVar.get() == "Bilinear":
                rotated_image = rotationObject.rotateImage_Bilinear()
                rotationType = "Bilinear"
            elif self.interpVar.get() == "Bicubic":
                rotated_image = rotationObject.rotateImage_Bicubic()
                rotationType = "Bicubic"
            else:
                rotated_image = rotationObject.rotateImage_NearestNeighbor()
                rotationType = "Nearest Neighbor"

            self.setOutputImageShape(rotated_image.shape)

            self.displayImageOnLabel(self.outputImageLabel, rotated_image, self.IMAGE_SIZE)

            self.outputImage = rotated_image
            interpolationType = self.interpVar.get()
            if interpolationType == "Interpolation":
                interpolationType = "Nearest_Neighbor"
            self.currentOutFileName = self.outFileInitialName + "_rotation_" + interpolationType \
                                      + "_" + str(self.retrieveRotationAngle())

            self.setStatus("Rotated image " + str(self.retrieveRotationAngle()) + "° using " + rotationType +
                            " interpolation.")

        elif self.transformationSelection.get() == 2:
            # scale
            scale_object = Scale()

            (N, M) = self.inputImage.shape

            try:
                scale_x = int(np.round(float(self.scaling_x_Entry.get())))
            except ValueError:
                scale_x = N

            try:
                scale_y = int(np.round(float(self.scaling_y_Entry.get())))
            except ValueError:
                scale_y = M


            scaled_image = scale_object.resize(self.inputImage, scale_x, scale_y, self.interpVar.get())

            self.displayImageOnLabel(self.outputImageLabel, scaled_image, self.IMAGE_SIZE)

            self.setOutputImageShape(scaled_image.shape)

            self.outputImage = scaled_image
            interpolationType = self.interpVar.get()
            if interpolationType == "Interpolation":
                interpolationType = "Nearest_Neighbor"
            self.currentOutFileName = self.outFileInitialName + "_scale_" + interpolationType \
                                      + "_height_" + str(self.scaling_x_Entry.get()) + "_width_" \
                                       + str(self.scaling_y_Entry.get())

            self.setStatus("Scaled image using " + interpolationType + " interpolation to: " + str(scale_x) \
                                   + " x " + str(scale_y) + " .")

        elif self.transformationSelection.get() == 3:
            # reflection
            print("Reflection Radio Button Selected")
            self.setStatus("Reflecting image.")

            reflectionObject = Reflection()

            axis = self.reflectionVar.get()

            if axis == "X-axis" or axis == "Reflection Type":
                reflected_image = reflectionObject.reflectOnAxisX(self.inputImage)
            elif axis == "Y-axis":
                reflected_image = reflectionObject.reflectOnAxisY(self.inputImage)
            else:
                reflected_image = self.inputImage

            self.displayImageOnLabel(self.outputImageLabel, reflected_image, self.IMAGE_SIZE)

            self.setOutputImageShape(reflected_image.shape)

            self.outputImage = reflected_image
            reflectionType = self.reflectionVar.get()
            if reflectionType == "Reflection Type":
                reflectionType = "X-axis"

            self.currentOutFileName = self.outFileInitialName + "_reflected_on_" + reflectionType

            self.setStatus("Reflected Image on " + reflectionType + ".")

        elif self.transformationSelection.get() == 4:
            # translation
            translate_object = Translate()

            try:
                translation_x = int(np.round(float(self.translation_x_Entry.get())))
            except ValueError:
                translation_x = 0

            try:
                translation_y = int(np.round(float(self.translation_y_Entry.get())))
            except ValueError:
                translation_y = 0

            
            translated_image = translate_object.translate(self.inputImage, translation_x, translation_y)
            translated_image_display = self.makeDisplayImage(translated_image, self.IMAGE_SIZE)
            self.setOutputImageShape(translated_image.shape)
            self.outputImageLabel.configure(image=translated_image_display)
            self.outputImageLabel.image = translated_image_display
            
            self.outputImage = translated_image
            self.currentOutFileName = self.outFileInitialName + "_translate_x_" \
                                      + str(translation_x) + "_y_" + str(translation_y)
            
            self.setStatus("Translating image: x: " + str(translation_x) + " , y: " + str(translation_y))
            


        elif self.transformationSelection.get() == 5:
            # shear
            shear_object = Shear()

            try:
                m_entry = float(self.shear_m_Entry.get())
            except ValueError:
                m_entry = 0.0
            
            sheared_image = shear_object.shear(self.inputImage, m_entry, self.shear_var.get(), self.interpVar.get())

            self.displayImageOnLabel(self.outputImageLabel, sheared_image, self.IMAGE_SIZE)

            self.setOutputImageShape(sheared_image.shape)

            self.outputImage = sheared_image

            interpolationType = self.interpVar.get()
            if interpolationType == "Interpolation":
                interpolationType = "Nearest_Neighbor"

            shearType = self.shear_var.get()
            if shearType == "Shear Type":
                shearType = "Vertical"
            self.currentOutFileName = self.outFileInitialName + "_shear_" + interpolationType \
                                      + "_m_" + str(m_entry) + "_type_" \
                                      + str(shearType)

            self.setStatus("Sheared image type: " + shearType + " using " + interpolationType \
                           + " interpolation with m = " + str(m_entry))

        else:
            self.setStatus("No image geometric transformation is selected.")


    def retrieveRotationAngle(self):
        rotationAngleString = self.rotationAngleEntry.get()
        rotationAngle = 0
        try:
            rotationAngle = float(rotationAngleString)
            self.setStatus("Setting rotation angle to " + str(rotationAngle) + "°")
        except ValueError:
            self.setStatus("Setting default rotation angle to 0°")
        return rotationAngle


    def setStatus(self, statusString):
        self.statusLabel.configure(text=statusString)
        self.statusLabel.text = statusString

    def setOutputImageShape(self, shape):
        """ set output image label string """
        image_shape_str = "Output Image Size: " + str(shape)
        self.outputImageShapeLabel.configure(text=image_shape_str)
        self.outputImageShapeLabel.text = image_shape_str

    def displayImageOnLabel(self, label, image, image_size):
        """ Display input image on input label"""
        displayImage = self.makeDisplayImageSquare(image, image_size)
        label.configure(image=displayImage)
        label.image = displayImage

    def makeDisplayImage(self, cv2_image, shape):
        disp_im = Image.fromarray(cv2_image)
        disp_im = disp_im.resize(shape, Image.ANTIALIAS)
        return ImageTk.PhotoImage(disp_im)

    def makeDisplayImageSquare(self, cv2_image, shape):
        square_image = self.makeImageSquare(cv2_image)
        disp_im = Image.fromarray(square_image)
        disp_im = disp_im.resize(shape, Image.ANTIALIAS)
        return ImageTk.PhotoImage(disp_im)

    def makeImageSquare(self, image):
        """ Return square image from non-square image if necessary """
        (N, M) = image.shape
        if N == M:
            return image
        elif N > M: # image is longer than it is wide
            difference = N - M
            left_offset = np.int(np.round(difference/2))
            right_offset = N - (difference - left_offset)
            #print("left_offset: ", left_offset, " right_offset: ", right_offset)
            squared_image = np.zeros((N, N), np.uint8)
            for ii in range(N):
                for jj in range(N):
                    if jj < left_offset or jj >= right_offset:
                        squared_image[ii][jj] = 255
                    else:
                        squared_image[ii][jj] = image[ii][jj - left_offset]
            #print("N > M: Squared Image shape: ", squared_image.shape)
            return squared_image

        else: # image is wider than it is long, M > N
            difference = M - N
            top_offset = np.int(np.round(difference/2))
            bot_offset = M - (difference - top_offset)
            #print("top_offset: ", top_offset, " bot_offset: ", bot_offset)
            squared_image = np.zeros((M, M), np.uint8)
            for ii in range(M):
                for jj in range(M):
                    if ii < top_offset or ii >= bot_offset:
                        squared_image[ii][jj] = 255
                    else:
                        squared_image[ii][jj] = image[ii - top_offset][jj]
            #print("N < M: Squared Image shape: ", squared_image.shape)
            return squared_image
        # N and M are None?
        print("Error making square image.")

    def doNothing(self):
        print("Not implemented yet.")




# start Project GUI
root = Tk()

p = ProjectMNQT_UI(root)

root.mainloop()

