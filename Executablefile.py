#!/usr/bin/env python
# coding: utf-8

# In[11]:

def findrts(p):
    import numpy as np
    for l in range(len(p)):
        if l == 0 and p[l] == 'x':
            p=p[:l]+'+1'+p[l:]
        if l == 1 and p[l] == 'x' and p[0]=='-':
            p=p[:l]+'1'+p[l:]
        if p[l] == 'x' and (p[l-1] == '-' or p[l-1]=='+'):
            p=p[:l]+'1'+p[l:]
        if p[0]!='-' and p[0]!='+':
            p=p[:l]+'+'+p[l:]
    print(p)
    op=p
    g=[]
    t=0

    for i in range(len(op)-1, 0-1, -1):
        if op[i] == "x" :
            for j in range(int(op[i+2])-t-1):
                g.insert(0,0)
            t=int(op[i+2])
            k,mul,val=i-1,1,0
            while(1):
                val=int(op[k])*mul+val
                k=k-1
                mul*=10
                if op[k]=='-' or op[k]=='+':
                    break
            if op[k]== '-':
                g.insert(0,-val)
            else:
                g.insert(0,val)
    k,mul,val=len(op)-1,1,0
    while(1):
        val=int(op[k])*mul+val
        k=k-1
        mul*=10
        if op[k]=='-' or op[k]=='+':
            break
    if op[k]== '-':
        g.append(-val)
    else:
        g.append(val)
    print(g)
    p=np.poly1d(g)
    res=p.r
    return res

def predic(num,model):
    import numpy as np
    import cv2
    img = cv2.imread('output.png',cv2.IMREAD_GRAYSCALE)

    if img is not None:
        img = ~img # Invert the bits of image 255 -> 0
        _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY) # Set bits > 127 to 1 and <= 127 to 0
        ctrs, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0]) # Sort by x

        img_data = []
        rects = []
        for c in cnt :
            x, y, w, h = cv2.boundingRect(c)
            rect = [x, y, w, h]
            rects.append(rect)

        bool_rect = []
        # Check when two rectangles collide
        for r in rects:
            l = []
            for rec in rects:
                flag = 0
                if rec != r:
                    if r[0] < (rec[0] + rec[2] + 10) and rec[0] < (r[0] + r[2] + 10) and r[1] < (rec[1] + rec[3] + 10) and rec[1] < (r[1] + r[3] + 10):
                        flag = 1
                    l.append(flag)
                else:
                    l.append(0)
            bool_rect.append(l)

        dump_rect = []
        # Discard the small collide rectangle
        for i in range(0, len(cnt)):
            for j in range(0, len(cnt)):
                if bool_rect[i][j] == 1:
                    area1 = rects[i][2] * rects[i][3]
                    area2 = rects[j][2] * rects[j][3]
                    if(area1 == min(area1,area2)):
                        dump_rect.append(rects[i])

        # Get the final rectangles
        final_rect = [i for i in rects if i not in dump_rect]
        for r in final_rect:
            x = r[0]
            y = r[1]
            w = r[2]
            h = r[3]

            im_crop = thresh[y:y+h+10, x:x+w+10] # Crop the image as most as possible
            im_resize = cv2.resize(im_crop, (28, 28)) # Resize to (28, 28)
            cv2.imshow("work",im_resize)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            im_resize = np.reshape(im_resize, (1, 28, 28)) # Flat the matrix
            img_data.append(im_resize)

    if num == "arithmetic":
        #print("Entered Aritha")
        operation = ''
        for i in range(len(img_data)):
            img_data[i] = np.array(img_data[i])
            img_data[i] = img_data[i].reshape(-1, 28, 28, 1)
            #print("Once")

            result = model.predict_classes(img_data[i])

            if result[0] == 10:
                operation += '-'
            elif result[0] == 11:
                operation += '+'
            elif result[0] == 12:
                operation += '*'
            elif result[0] == 13:
                operation += '*'
            else:
                operation += str(result[0])
       # print("String Found:", operation)
        res=eval(operation)
        return res
    else:
        operation=''
        #print("Entered poly")
        for i in range(len(img_data)):
            img_data[i] = np.array(img_data[i])
            img_data[i] = img_data[i].reshape(-1, 28, 28, 1)

            result = np.argmax(model.predict(img_data[i]),axis=-1)
    
            if result[0] == 10:
                operation += '-'
            elif result[0] == 11:
                operation += '+'
            elif result[0] == 12:
                operation += 'x'
            elif result[0] == 13:
                operation += 'x'
            elif result[0] == 1:
                operation += '1'         
            else:
                if len(operation) != 0 and operation[-1] == 'x':
                    operation += '^'
                    operation += str(result[0])
                else:    
                    operation += str(result[0])
        print(operation)
        n=len(operation)-1
        while operation[n]!='x':
            n=n-1
        if operation[n+1]!='^':
            operation=operation[:n+1]+"^1"+operation[n+1:]
        res=findrts(operation)
        return res




# In[ ]:




