from collections import deque
import numpy as np
import argparse
import imutils
import cv2

'''ap = argparse.ArgumentParser()
ap.add_argument("-v",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())'''
#синий
#lower1 = (61, 138, 152)
#upper1 = (86, 255, 255)

#lower2 = (33, 129, 157)
#upper2 = (119, 255, 255)

#lower1 = (0, 131, 145)
#upper1 = (63, 197, 192)
#мандарин
#lower2 = (0, 131, 145)
#upper2 = (63, 197, 192)
#желтый
lower3 = (63, 51, 0)
upper3 = (96, 255, 255)
#розовый
lower4 = (124, 42, 159)
upper4 = (183, 185, 222)
#pts = deque(maxlen=args["buffer"])


lower1 = (33, 155, 117)
upper1 = (122, 255, 255)

lower2 = (0, 131, 145)
upper2 = (63, 197, 192)

camera = cv2.VideoCapture(0)



# keep looping
while True :
	# grab the current frame
	(grabbed, frame1) = camera.read()
	#(grabbed, frame2) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	#if args.get("video") and not grabbed:
		#break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	#frame = #imutils.resize(frame, width=600)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
	#hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask1 = cv2.inRange(hsv, lower1, upper1)
	mask1 = cv2.erode(mask1, None, iterations=2)
	mask1 = cv2.dilate(mask1, None, iterations=2)
	#print("      ", mask1)
	mask2 = cv2.inRange(hsv, lower2, upper2)
	mask2 = cv2.erode(mask2, None, iterations=2)
	mask2 = cv2.dilate(mask2, None, iterations=2)

	mask3 = cv2.inRange(hsv, lower3, upper3)
	mask3 = cv2.erode(mask3, None, iterations=2)
	mask3 = cv2.dilate(mask3, None, iterations=2)

	mask4 = cv2.inRange(hsv, lower4, upper4)
	mask4 = cv2.erode(mask4, None, iterations=2)
	mask4 = cv2.dilate(mask4, None, iterations=2)
	#print(mask2)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	mask = mask1 + mask2 + mask3 + mask4
	cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	cnts3 = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	cnts4 = cv2.findContours(mask4.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]

	center1 = None
	center2 = None
	center3 = None
	center4 = None

	# only proceed if at least one contour was found
	if len(cnts1) > 0  and len(cnts2) > 0 and len(cnts3) > 0 and len(cnts4) > 0 :
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c1 = max(cnts1, key=cv2.contourArea)
		#print(cnts2)
		c2 = max(cnts2, key=cv2.contourArea)

		c3 = max(cnts3, key=cv2.contourArea)

		c4 = max(cnts4, key=cv2.contourArea)

		((x1, y1), radius1) = cv2.minEnclosingCircle(c1)

		((x2, y2), radius2) = cv2.minEnclosingCircle(c2)

		((x3, y3), radius3) = cv2.minEnclosingCircle(c3)

		((x4, y4), radius4) = cv2.minEnclosingCircle(c4)

		M1 = cv2.moments(c1)

		M2 = cv2.moments(c2)

		M3 = cv2.moments(c3)

		M4 = cv2.moments(c4)
		center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))

		center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))

		center3 = (int(M3["m10"] / M3["m00"]), int(M3["m01"] / M3["m00"]))

		center4 = (int(M4["m10"] / M4["m00"]), int(M4["m01"] / M4["m00"]))
		print(center1, "            ", center2, "            ",center3 ,"            ", center4)
		# only proceed if the radius meets a minimum size
		if radius1 > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame1, (int(x1), int(y1)), int(radius1),
				(255, 255, 0), 2)
			#Красные точки
			#cv2.circle(frame1, center1, 5, (0, 0, 0), -1)
			cv2.circle(frame1, center1, 5, (0, 0, 255), -1)
			#Поменять
			if radius2 > 10:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame1, (int(x2), int(y2)), int(radius2),
					(255, 255, 0), 2)
				cv2.circle(frame1, center2, 5, (0, 0, 255), -1)
				if radius3 > 10:
					# draw the circle and centroid on the frame,
					# then update the list of tracked points
					cv2.circle(frame1, (int(x3), int(y3)), int(radius3),
							   (255, 255, 0), 2)
					cv2.circle(frame1, center3, 5, (0, 0, 255), -1)
					if radius4 > 10:
						# draw the circle and centroid on the frame,
						# then update the list of tracked points
						cv2.circle(frame1, (int(x4), int(y4)), int(radius4),
								   (255, 255, 0), 2)
						cv2.circle(frame1, center4, 5, (0, 0, 255), -1)
	# update the points queue
	#pts.appendleft(center)
	# loop over the set of tracked points
	xrange = range
	'''
	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = 0
		#int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
		'''




	# show the frame to our screen
	cv2.imshow("VIDEO", frame1)
	#cv2.imshow("Frame", frame2)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("z") or key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()