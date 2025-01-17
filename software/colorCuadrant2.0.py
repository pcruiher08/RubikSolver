import cv2
import cv2.aruco as aruco
import numpy as np
import os
from polygon import Polygon 
import math as m 


button = Polygon(np.array(list(map(list, [(0,0),(0,20),(20,20),(20,0)]))), (0,255,0))
scanState = 0

polygonsState0 = []
polygonsState1 = []
polygonsState2 = []


def finiteStateMachine(event,x,y,flags,param):
    global scanState, polygonsState0, polygonsState1, polygonsState2
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        print(x,y)
        if pointInsidePolygon((x,y), button.getCoordinates()):
            scanState += 1
            print("cambio de estado", scanState)
        if scanState == 0:
            print("finiteStateMachine", scanState)
            print("desde la funcion", polygonsState0)
            #print((x,y), polygonsState0[0].egtCoordinates())
            for polygon in polygonsState0:
                if pointInsidePolygon((x,y), polygon.getCoordinates()):
                    polygon.nextColor()
                    #print("desde la funcion", polygon.getColorLetter())
        elif scanState == 1:
            print("finiteStateMachine", scanState)
        elif scanState == 2:
            print("finiteStateMachine", scanState)
        elif scanState == 3:
            print("finiteStateMachine", scanState)
        elif scanState == 4:
            print("finiteStateMachine", scanState)
        elif scanState == 5:
            print("finiteStateMachine", scanState)
        elif scanState == 6:
            print("finiteStateMachine", scanState)
        elif scanState == 7:
            print("finiteStateMachine", scanState)
        elif scanState == 8:
            print("finiteStateMachine", scanState)
        elif scanState == 9:
            #resolver
            print("a resolver")

def getMidPoint(a, b):
    return (int((a[0] + b[0]) / 2), int((a[1] + b[1]) / 2))

def getThirdPoint(a, b):
    return (int((a[0] + b[0]) / 3), int((a[1] + b[1]) / 3))

def getTwoThirdsPoint(a, b):
    return (int((a[0] + b[0]) * 2 / 3), int((a[1] + b[1]) * 2 / 3))

def getFractionPoint(a, b, t):
    return ( int(a[0] * (1 - t) ) + int(b[0] * t), int( a[1] * (1 - t) ) + int(b[1] * t) )

def distancePointPoint(a, b):
    return int( m.sqrt( (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]) ) )

def pointInterceptPointPointPointPoint(a, b, c, d):
    divide = (a[0] - b[0]) * (c[1] - d[1]) - (a[1] - b[1]) * (c[0] - d[0])
    punto1 = ((a[0]*b[1] - a[1]*b[0]) * (c[0]-d[0]) - (a[0]-b[0]) * (c[0]*d[1] - c[1]*d[0]))/divide
    punto2 = ((a[0]*b[1] - a[1]*b[0]) * (c[1]-d[1]) - (a[1]-b[1]) * (c[0]*d[1] - c[1]*d[0]))/divide
    return (int(punto1), int(punto2))

def calculateHSVDistance(a, b):
    dh = min(abs(b[0]-a[0]), 360-abs(b[0]-a[0])) / 180.0
    ds = abs(b[1]-a[1])
    dv = abs(b[2]-b[0]) / 255.0
    return m.sqrt(dh*dh+ds*ds+dv*dv)

def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

def pointInsidePolygon(point, polygon):
    isInsideRight = True
    isInsideLeft = True
    #print("estoy checando ", polygon, "con ", point)
    for i in range(len(polygon)):
        result = (point[1] - polygon[i][1]) * (polygon[(i + 1) % len(polygon)][0] - polygon[i][0]) - (point[0] - polygon[i][0]) * (polygon[(i + 1) % len(polygon)][1] - polygon[i][1])
        if(not (result < 0)):
            isInsideRight = False

    for i in range(len(polygon)):
        result = (point[1] - polygon[i][1]) * (polygon[(i + 1) % len(polygon)][0] - polygon[i][0]) - (point[0] - polygon[i][0]) * (polygon[(i + 1) % len(polygon)][1] - polygon[i][1])
        if(not (result > 0)):
            isInsideLeft = False
  
    return isInsideRight or isInsideLeft


def findArucoMarkers(img, markerSize = 4, totalMarkers=250, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    # print(ids)
    if draw:
        aruco.drawDetectedMarkers(img, corners,ids) 
    return [corners, ids]


def drawPolygons(img, overlay, polygons):
    for polygon in polygons:
        polygon.paintPolygonLines(img)
        polygon.fillPolygon(img, overlay)




cap = cv2.VideoCapture(0)   
greenColor = (0,255,0)
blueColor = (255,0,0)
redColor = (0,0,255)




while True:
    success, img = cap.read()
    #img = cv2.imread("2.55.jpg")
    orig = img.copy()
    arucofound = findArucoMarkers(img)
    howManyArucos = len(arucofound[0])
    if howManyArucos!=0:
        coordinates = []
        for bbox, id in zip(arucofound[0], arucofound[1]):
            #print(bbox, id)
            coords = tuple(bbox[0][0])
            #print(coords)
            coordinates.append(coords)
            #img = cv2.circle(img, coords, 2, redColor, 5)
        if(howManyArucos == 2):
            topCorner = getMidPoint(coordinates[0], coordinates[1])
            topCorner = (topCorner[0]-5, topCorner[1]+22)
            bottomCorner = (topCorner[0]-5, topCorner[1]+170)
            rightCorner = (bottomCorner[0]+125, bottomCorner[1]+40)
            leftCorner = (bottomCorner[0]-120, bottomCorner[1]+37)

            #central line
            img = cv2.line(img, topCorner, bottomCorner,[0,0,0],8)
            #right line
            img = cv2.line(img, bottomCorner, rightCorner,[0,0,0],8)
            #left line
            img = cv2.line(img, bottomCorner, leftCorner,[0,0,0],8)

            P1 = leftCorner
            P2 = getFractionPoint(bottomCorner, leftCorner, 2/3)
            P3 = getFractionPoint(bottomCorner, leftCorner, 1/3)
            P4 = bottomCorner
            P5 = getFractionPoint(bottomCorner, topCorner, 1/3+0.05) 
            P6 = getFractionPoint(bottomCorner, topCorner, 2/3+0.05)
            P7 = topCorner
            P8 = getFractionPoint(bottomCorner, rightCorner, 1/3 + 0.05)
            P9 = getFractionPoint(bottomCorner, rightCorner, 2/3 + 0.05)
            P10 = rightCorner 
            P11 = (P1[0]+8, P1[1] - distancePointPoint(P4, P5)+10) 
            P12 = getFractionPoint(P11, P5, 1/3)
            P15 = (P3[0]+7, P3[1] - distancePointPoint(bottomCorner, topCorner)+7)
            P13 = pointInterceptPointPointPointPoint(P3,P15,P5,P11)
            P14 = getFractionPoint(P15, P3, 1/3 - 0.05)
            P16 = (P8[0] + 2, P8[1] - distancePointPoint(topCorner, bottomCorner) + 5)
            P17 = getFractionPoint(P16, P8, 1/3 - 0.05)
            P20 = (P5[0] + distancePointPoint(bottomCorner, rightCorner) - 10, P5[1] + distancePointPoint(P5, P4) - 13)
            P18 = pointInterceptPointPointPointPoint(P8,P16,P5,P20)
            P19 = getFractionPoint(P5, P20, 2/3 + 0.08)
            P21 = (P1[0] + distancePointPoint(P4,P5)-7, P1[1] + 16)
            P22 = getFractionPoint(P21, P8, 1/3-0.05)
            P25 = (P10[0]-35, P1[1]+20)
            P23 = pointInterceptPointPointPointPoint(P3,P25,P8,P21)
            P24 = getFractionPoint(P25, P3, 1/3)
            overlay = img.copy()

            button.fillPolygon(img,overlay)
            C1 = Polygon(np.array(list(map(list, [P1, P11, P12, P2]))), (255,255,255)) 
            C2 = Polygon(np.array(list(map(list, [P2, P12, P13, P3]))), (255,255,255))
            C3 = np.array(list(map(list, [P3, P13, P5, P4])))
            C4 = np.array(list(map(list, [P4, P5, P18, P8])))
            C5 = np.array(list(map(list, [P8, P18, P19, P9])))
            C6 = np.array(list(map(list, [P9, P19, P20, P10])))
            C7 = np.array(list(map(list, [P13, P14, P6, P5])))
            C8 = np.array(list(map(list, [P14, P15, P7, P6])))
            C9 = np.array(list(map(list, [P6, P7, P16, P17])))
            C10 = np.array(list(map(list, [P5, P6, P17, P18])))
            C11 = np.array(list(map(list, [P21, P1, P2, P22])))
            C12 = np.array(list(map(list, [P22, P2, P3, P23])))
            C13 = np.array(list(map(list, [P23, P3, P4, P8])))
            C14 = np.array(list(map(list, [P23, P8, P9, P24])))
            C15 = np.array(list(map(list, [P24, P9, P10, P25])))

            #cv2.setMouseCallback('img',finiteStateMachine)

            polygonsState0 = [C1, C2, C3, C4]
                            
            alpha = 0.5

            #cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)


            '''
            img = cv2.circle(img, P1, 2, blueColor, 5)
            img = cv2.circle(img, P2, 2, blueColor, 5)
            img = cv2.circle(img, P3, 2, blueColor, 5)
            img = cv2.circle(img, P4, 2, blueColor, 5)
            img = cv2.circle(img, P5, 2, blueColor, 5)
            img = cv2.circle(img, P6, 2, blueColor, 5)
            img = cv2.circle(img, P7, 2, blueColor, 5)
            img = cv2.circle(img, P8, 2, blueColor, 5)
            img = cv2.circle(img, P9, 2, blueColor, 5)
            img = cv2.circle(img, P10, 2, blueColor, 5)
            img = cv2.circle(img, P11, 2, blueColor, 5)
            img = cv2.circle(img, P12, 2, blueColor, 5)
            img = cv2.circle(img, P13, 2, blueColor, 5)
            img = cv2.circle(img, P14, 2, blueColor, 5)
            img = cv2.circle(img, P15, 2, blueColor, 5)
            img = cv2.circle(img, P16, 2, blueColor, 5)
            img = cv2.circle(img, P17, 2, blueColor, 5)
            img = cv2.circle(img, P18, 2, blueColor, 5)
            img = cv2.circle(img, P19, 2, blueColor, 5)
            img = cv2.circle(img, P20, 2, blueColor, 5)
            img = cv2.circle(img, P21, 2, blueColor, 5)
            img = cv2.circle(img, P22, 2, blueColor, 5)
            img = cv2.circle(img, P23, 2, blueColor, 5)
            img = cv2.circle(img, P24, 2, blueColor, 5)
            img = cv2.circle(img, P25, 2, blueColor, 5)
            '''
            #lineas especiales
            
            img = cv2.line(img, P5, P20,[0,0,0],4)
            img = cv2.line(img, P8, P16,[0,0,0],4)
            img = cv2.line(img, P10, P20,[0,0,0],4)
            img = cv2.line(img, P7, P16,[0,0,0],4)
            img = cv2.line(img, P6, P17,[0,0,0],4)
            img = cv2.line(img, P9, P19,[0,0,0],4)
            img = cv2.line(img, P3, P15,[0,0,0],4)
            img = cv2.line(img, P5, P11,[0,0,0],4)
            img = cv2.line(img, P1, P11,[0,0,0],4)
            img = cv2.line(img, P15, P7,[0,0,0],4)
            img = cv2.line(img, P6, P14,[0,0,0],4)
            img = cv2.line(img, P2, P12,[0,0,0],4)
            img = cv2.line(img, P8, P21,[0,0,0],4)
            img = cv2.line(img, P3, P25,[0,0,0],4)
            img = cv2.line(img, P10, P25,[0,0,0],4)
            img = cv2.line(img, P1, P21,[0,0,0],4)
            img = cv2.line(img, P2, P22,[0,0,0],4)
            img = cv2.line(img, P9, P24,[0,0,0],4)


            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            edgee = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            #cv2.imshow('1', img)

            edge = cv2.Canny(edgee,100,200)
            #cv2.imshow("e",edge)

            rows,cols,dim = img.shape
            out = np.zeros([rows, cols, dim], dtype=np.uint8)
            acumm = mask = np.zeros((rows, cols), dtype=np.uint8)

            low_red = np.array([0,50,50])
            upper_red = np.array([10,255,255])

            color_ranges_HSV = [
                [(179, 59, 255), (0, 0, 106),"W"],
                [(20, 255, 255), (9, 58, 33),"O"],
                [(89, 255, 255), (36, 50, 70),"G"],
                [(180, 255, 255), (159, 50, 70),"R"],
                [(8, 255, 255), (0, 45, 0),"R"],
                [(35, 255, 255), (25, 50, 70),"Y"],
                [(120, 255, 255), (50, 90, 135),"B"]
            ]
            contoursFinal = []
            maskTemp = np.zeros([rows,cols,3],np.uint8)
            for i in range(len(color_ranges_HSV)):
                mask = cv2.inRange(hsv,color_ranges_HSV[i][1],color_ranges_HSV[i][0])
                ret, thresh = cv2.threshold(mask,127,255,0)
                #cv2.imshow(color_ranges_HSV[i][2],mask)
                contours, hier = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                contours = polygonsState0
                for j in range(len(contours)):
                    if(cv2.contourArea(contours[j]) > 300 and cv2.contourArea(contours[j]) < 3000):
                        epsilon = 0.1*cv2.arcLength(contours[j],True)
                        aprox = cv2.approxPolyDP(contours[j], 3, True)
                        #cv2.drawContours(img,contours[j],-1,(255,0,0),3)
                        if(cv2.contourArea(aprox) > 300):
                            mask = np.zeros([rows,cols],np.uint8)
                            cv2.drawContours(mask,[aprox],-1,255,-1)
                            mean = cv2.mean(hsv,mask=mask)
                            temp = np.zeros([1,1,3],np.uint8)
                            temp[0][0] = mean[:3]
                            #print(mean)
                            cv2.drawContours(img,[aprox],-1,[0,0,255],3)
                            #cv2.drawContours(img,[aprox],-1,mean[:2],3)
                            cv2.imshow("hola2",img)
                            #cv2.fillPoly(img,pts = [aprox], color = mean)
                            for k in range(len(color_ranges_HSV)):
                                inR = cv2.inRange(temp,color_ranges_HSV[k][1],color_ranges_HSV[k][0])
                                if(inR[0][0] == 255):
                                    #cv2.drawContours(maskTemp,[aprox],-1,mean,3)
                                    contoursFinal.append([[aprox],color_ranges_HSV[k][2]])
                                    cv2.fillPoly(maskTemp,pts = [aprox], color = mean)
            maskTemp = cv2.cvtColor(maskTemp, cv2.COLOR_HSV2BGR)
            cv2.imshow("maske",maskTemp)
            cv2.imshow("holaaaa",orig)
            print(contoursFinal)




            '''
            cv2.fillPoly(overlay, pts = [C1], color =tuple(getAverageInsidePolygon(img,C1)[0]))
            cv2.fillPoly(overlay, pts = [C2], color =tuple(getAverageInsidePolygon(img,C2)[0]))
            cv2.fillPoly(overlay, pts = [C3], color =tuple(getAverageInsidePolygon(img,C3)[0]))
            cv2.fillPoly(overlay, pts = [C4], color =tuple(getAverageInsidePolygon(img,C4)[0]))
            cv2.fillPoly(overlay, pts = [C5], color =tuple(getAverageInsidePolygon(img,C5)[0]))
            cv2.fillPoly(overlay, pts = [C6], color =tuple(getAverageInsidePolygon(img,C6)[0]))
            cv2.fillPoly(overlay, pts = [C7], color =tuple(getAverageInsidePolygon(img,C7)[0]))
            cv2.fillPoly(overlay, pts = [C8], color =tuple(getAverageInsidePolygon(img,C8)[0]))
            cv2.fillPoly(overlay, pts = [C9], color =tuple(getAverageInsidePolygon(img,C9)[0]))
            cv2.fillPoly(overlay, pts = [C10], color =tuple(getAverageInsidePolygon(img,C10)[0]))
            cv2.fillPoly(overlay, pts = [C11], color =tuple(getAverageInsidePolygon(img,C11)[0]))
            cv2.fillPoly(overlay, pts = [C12], color =tuple(getAverageInsidePolygon(img,C12)[0]))
            cv2.fillPoly(overlay, pts = [C13], color =tuple(getAverageInsidePolygon(img,C13)[0]))
            cv2.fillPoly(overlay, pts = [C14], color =tuple(getAverageInsidePolygon(img,C14)[0]))
            cv2.fillPoly(overlay, pts = [C15], color =tuple(getAverageInsidePolygon(img,C15)[0]))
            '''




    cv2.imshow('img',img)

    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
#cap.release()
cv2.destroyAllWindows()