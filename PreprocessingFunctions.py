#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 09:19:00 2022

@author: mshah
"""

'''
You will need to create folders before running each function. Example usage below:
    
    from PreprocessingFunctions import *
    
    P1 = '/Users/mshah/Downloads/8_24_Test2/'  <---- Main Folder
    S1 = '/Users/mshah/Downloads/8_24_Test2/Split/'  <---- Must make this folder
    F1 = '/Users/mshah/Downloads/8_24_Test2/Filtered/'  <---- Must make this folder
    M1 = '/Users/mshah/Downloads/8_24_Test2/Masks/'  <---- Must make this folder
    I1 = '/Users/mshah/Downloads/8_24_Test2/Images/'  <---- Must make this folder
    
    renameFiles(P1)
    convertTIFtoJPG(P1)
    resizeImages(P1)
    splitImages(P1, S1)
    filterBlankImages(S1, F1)
    binarizeMasks(S1)
    padFiles(S1)
    sortImages(S1, M1, I1)
    
'''




import os
import cv2
from PIL import Image
import numpy as np
from numpy import asarray

def renameFiles(inputPath, outputPath = "Same"):
    if outputPath == "Same":
        outputPath = inputPath
    for I1 in os.listdir(inputPath):
        if I1.endswith(".png") or I1.endswith(".jpg") or I1.endswith(".tif"):
            I2 = I1.replace(" ", "_")
            os.rename(inputPath + I1, outputPath + I2)
            
def convertTIFtoJPG(inputPath, outputPath = "Same"):
    if outputPath == "Same":
        outputPath = inputPath
    for I1 in os.listdir(inputPath):
        if I1.endswith(".tif"):
            I2 = I1.split(".tif")[0]
            I3 = I2 + ".jpg"
            os.rename(inputPath + I1, outputPath + I3)

def binarizeMasks(inputPath, outputPath = "Same"):
    thresh = 1
    if outputPath == "Same":
        outputPath = inputPath
    for M1 in os.listdir(inputPath):
        if M1.endswith(".png") and not M1.startswith('.'):
            M2 = cv2.imread(inputPath + M1, 0)
            M3 = cv2.threshold(M2, thresh, 1, cv2.THRESH_BINARY)[1]
            cv2.imwrite(outputPath + M1, M3)
            
def resizeImages(inputPath, outputPath = "Same", size = (1500,1500)):
    if outputPath == "Same":
        outputPath = inputPath
    for I1 in os.listdir(inputPath):
        if I1.endswith(".png") or I1.endswith(".jpg") or I1.endswith(".tif"):
            I2 = Image.open(inputPath + I1)
            I2 = I2.resize(size)
            I2.save(outputPath + I1)

def splitImages(inputPath, outputPath = "Same", size = (150,150)):
    if outputPath == "Same":
        outputPath = inputPath
    for I1 in os.listdir(inputPath):
        if I1.endswith(".png") or I1.endswith(".jpg") or I1.endswith(".tif"):
            I2 = Image.open(inputPath + I1)
            data = asarray(I2)
            tiles = [data[x:x+size[0],y:y+size[1]] for x in range(0,data.shape[0],size[0]) for y in range(0,data.shape[1],size[1])]
            i = 0
            for tile in tiles:
                tile = tile.astype('uint8')
                Image.fromarray(tile).save(outputPath + str(i) + '_' + I1)
                i += 1
                
def sortImages(inputPath, maskOutputPath, imgOutputPath):
    for F1 in os.listdir(inputPath):
        if F1.endswith(".png"):
            os.rename(inputPath + F1, maskOutputPath + F1)        
        if F1.endswith(".tif") or F1.endswith(".jpg"):
            os.rename(inputPath + F1, imgOutputPath + F1)

def filterBlankImages(maskInputPath, maskOutputPath, imgType = '.jpg', imgInputPath = "Same", imgOutputPath = "Same"):
    if imgInputPath == "Same":
        imgInputPath = maskInputPath
    if imgOutputPath == "Same":
            imgOutputPath = maskOutputPath    
    for M1 in os.listdir(maskInputPath):
        if M1.endswith(".png"):
            M2 = Image.open(maskInputPath + M1)
            data = asarray(M2)
            data_sum = np.sum(data)
            if data_sum == 0:
                I1 = M1.split("_cp")[0]
                I2 = I1 + imgType
                os.rename(imgInputPath + I2, imgOutputPath + I2)
                os.rename(maskInputPath + M1, maskOutputPath + M1)
        
def padFiles(maskInputPath, maskOutputPath = "Same", imgInputPath = "Same", imgOutputPath = "Same", padding = "symmetric", padSize = (5,5)):
    if maskOutputPath == "Same":
        maskOutputPath = maskInputPath
    if imgInputPath == "Same" and imgOutputPath == "Same":
        imgInputPath = maskInputPath
        imgOutputPath = maskOutputPath
        for M1 in os.listdir(maskInputPath):
            if M1.endswith(".png") and not M1.startswith("."):
                M2 = Image.open(maskInputPath + M1)
                M3 = asarray(M2)
                M4 = np.pad(M3, ((padSize[0],padSize[1]),(padSize[0],padSize[1])), mode=padding)
                Image.fromarray(M4).save(maskOutputPath + M1)
        for I1 in os.listdir(imgInputPath):
            if I1.endswith(".jpg") or I1.endswith(".tif") and not I1.startswith("."):
                I2 = Image.open(imgInputPath + I1)
                I2 = I2.convert('RGB')
                I3 = asarray(I2)
                I4 = np.pad(I3, ((padSize[0],padSize[1]),(padSize[0],padSize[1]),(0,0)), mode=padding)
                Image.fromarray(I4).save(imgOutputPath + I1)
    else:
        for M1 in os.listdir(maskInputPath):
            if M1.endswith(".png") and not M1.startswith("."):
                M2 = Image.open(maskInputPath + M1)
                M3 = asarray(M2)
                M4 = np.pad(M3, ((padSize[0],padSize[1]),(padSize[0],padSize[1])), mode=padding)
                Image.fromarray(M4).save(maskOutputPath + M1)
        for I1 in os.listdir(imgInputPath):
            if I1.endswith(".jpg") or I1.endswith(".tif") and not I1.startswith("."):
                I2 = Image.open(imgInputPath + I1)
                I2 = I2.convert('RGB')
                I3 = asarray(I2)
                I4 = np.pad(I3, ((padSize[0],padSize[1]),(padSize[0],padSize[1]),(0,0)), mode=padding)
                Image.fromarray(I4).save(imgOutputPath + I1)