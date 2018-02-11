import cairo,argparse,random

#TEST: https://jcmellado.github.io/js-aruco/getusermedia/getusermedia.html
#http://terpconnect.umd.edu/~jwelsh12/enes100/markergen.html
#http://terpconnect.umd.edu/~jwelsh12/enes100/markers.js
markers_opts = [[False,True,True,True,True],[False,True,False,False,False]
                   ,[True,False,True,True,False],[True,False,False,False,True]];
import string
digs = string.digits + string.letters

def int2base(x, base):
  if x < 0: sign = -1
  elif x == 0: return digs[0]
  else: sign = 1
  x *= sign
  digits = []
  while x:
    digits.append(digs[x % base])
    x /= base
  if sign < 0:
    digits.append('-')
  digits.reverse()
  return ''.join(digits)

def drawMarker(canvas,id,sw,sh,x,y):
    id = int2base(id,4).zfill(5) # 0 padded 5 digits
    rows = [int(q) for q in id] # as integers
    #print "marker",id,"at",x,y,"sized",sw,sh,rows
    sw = sw/7.0
    sh = sh/7.0
    #val = padDigits(Number(id).toString(4),5);
    #rows = /(\d)(\d)(\d)(\d)(\d)/.exec(val).slice(1,6);
    #ctx = canvas.getContext('2d');
    #pad = canvas.pad;// || 15;
    #sw=(canvas.width - (pad*2))/7;
    #sh=(canvas.height - (pad*2))/7;
    #background white
    for h in range(0,7):
        for w in range(0,7):
            if (w==0 or h==0 or h==6 or w==6):
                black = True
            elif markers_opts[rows[h - 1]][w - 1]:
                black = True
            else:
                black = False
            # draw rectangle at ... w*sw+pad h*sh+pad sized sw,sh
            # filled and stroken in white or black ...
            if black:
                ctx.set_source_rgb(0,0,0)
            else:
                #continue
                ctx.set_source_rgb(1,1,1)
            ctx.rectangle(w*sw + x,h*sh + y,sw,sh);
            ctx.stroke();
            ctx.rectangle(w*sw + x,h*sh + y,sw,sh);
            ctx.fill();


if __name__ == '__main__':
    import argparse

    print 'aruco board generator'
    pages = dict(A4=(210,297),A3=(297,420))

    parser = argparse.ArgumentParser(description='Aruco Page Maker to PDF, Emanuele Ruffaldi 2015')
    parser.add_argument('--page', default="A4", help='page size: A4 or A3')
    parser.add_argument('--pages',default=1,type=int,help="number of pages")
    parser.add_argument('--landscape', dest='landscape', action='store_const',const=True,default=False,help="set landscape")
    parser.add_argument('--portrait', dest='landscape', action='store_const',const=False,default=False,help="set landscape")
    parser.add_argument('--markersize', type=float,default=35,help="marker size (mm)")
    parser.add_argument('--bordersize', type=float, default=5,help="bourder around marker (mm)")
    parser.add_argument('--spacing', type=float,default=2,help="marker spacing in vertical and horizontal (mm)")
    parser.add_argument('--pagemargin', type=float,default=10,help="spacing default around (mm)")
    parser.add_argument('--fill', action="store_true",help="fills the page")
    parser.add_argument('--rows', type=int,default=6,help="fill rows")
    parser.add_argument('--cols', type=int,default=4,help="fill cols")
    parser.add_argument('--first', type=int,default=50,help="first id")
    parser.add_argument('--last', type=int,default=100,help="last id")
    parser.add_argument('--repeat', type=bool,default=False,help="repeat mode (ends at last)")
    parser.add_argument('--count', type=int,default=0,help="count (alternative to last)")
    parser.add_argument('--border', action='store_true',help="draws black border around")
    parser.add_argument('--pageborder', action='store_true',help="draws black border around")
    parser.add_argument('--axis', action='store_true',help="highlights axis")
    parser.add_argument('--random', action='store_true',help="randomize markers for board (and produces the randomization)")
    parser.add_argument('--output',default="output.pdf",help="outputfilename")


    args = parser.parse_args()

    page = pages[args.page]
    if args.landscape:
        page = (page[1],page[0])
    if args.count != 0:
        args.last = args.first + args.count - 1
    else:
        args.count = args.last - args.first + 1

    mm2pts = 2.83464567
    lw = 0.5 # mm
    lwdef = 0.5
    bordercolor = (0.5,0.5,0.5)
    if args.fill:
        args.cols = (page[0]-args.pagemargin*2)/(args.markersize+args.bordersize*2+args.spacing)
        args.rows = (page[1]-args.pagemargin*2)/(args.markersize+args.bordersize*2+args.spacing)
        print "fill results in rows x cols",args.rows,args.cols

    bid = 0

    width_pts, height_pts = page[0]*mm2pts,page[1]*mm2pts
    surface = cairo.PDFSurface (args.output, width_pts, height_pts)
    ctx = cairo.Context (surface)
    ctx.scale(mm2pts,mm2pts)
    done = False

    n = args.pages*args.rows*args.cols
    if args.count < n:
        n = args.count
    markers = [args.first+i for i in range(0,n)]
    if args.random:
        random.shuffle(markers)
        open(args.output+".txt","w").write(" ".join([str(x) for x in markers]))

    for p in range(0,args.pages):
        if done:
            break
        if args.pageborder:
            ctx.set_source_rgb(*bordercolor)
            ctx.set_line_width(lw)
            ctx.rectangle(args.pagemargin,args.pagemargin,page[0]-args.pagemargin*2,page[1]-args.pagemargin*2)
            ctx.set_line_width(lwdef) # default
            ctx.stroke()
        y = args.pagemargin
        for r in range(0,args.rows):
            x = args.pagemargin
            if done:
                break
            for c in range(0,args.cols):
                id = markers[bid % len(markers)]
                if not args.repeat and bid >= len(markers):
                    done = True
                    break
                drawMarker(ctx,id,args.markersize,args.markersize,x + args.bordersize,y + args.bordersize)
                bid = bid + 1
                if args.border:
                    ctx.set_source_rgb(*bordercolor)
                    ctx.set_line_width(lw)
                    ctx.rectangle(x,y,args.markersize + args.bordersize*2,args.markersize + args.bordersize*2)
                    ctx.set_line_width(lwdef) # default
                    ctx.stroke()
                if args.axis:
                    ctx.set_source_rgb(0, 0, 0)
                    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL,         cairo.FONT_WEIGHT_NORMAL)
                    (ax, ay, awidth, aheight, adx, ady) = ctx.text_extents("y>")
                    ctx.move_to(x + args.markersize -ax/mm2pts+args.bordersize-awidth/mm2pts,y-aheight*0.4)
                    ctx.show_text("y>")
                    (ax, ay, awidth, aheight, adx, ady) = ctx.text_extents("y")
                    ry0 = y +aheight*0.6 + args.markersize
                    rx0 = x + -awidth*1.2
                    ctx.move_to(rx0, ry0)
                    #ctx.show_text("v")
                    ry0 += aheight
                    ctx.move_to(rx0, ry0)
                    ctx.show_text("x")
                    ry0 += aheight
                    ctx.move_to(rx0, ry0)
                    ctx.show_text("v")
                x = x + args.bordersize*2+args.markersize + args.spacing
            y = y + args.markersize + args.bordersize*2 + args.spacing
        ctx.show_page()
