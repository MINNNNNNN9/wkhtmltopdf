#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 09:15:13 2019
@author: chenghan
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import numpy as np
from io import BytesIO




import math


class getHRVPlot:
    def realign_polar_xticks(self,ax):
        for theta, label in zip(ax.get_xticks(), ax.get_xticklabels()):
            theta = theta * ax.get_theta_direction() + ax.get_theta_offset()
            theta = np.pi/2 - theta
            y, x = np.cos(theta), np.sin(theta)
            if x >= 0.1:
                label.set_horizontalalignment('left')
            if x <= -0.1:
                label.set_horizontalalignment('right')
            if y >= 0.5:
                label.set_verticalalignment('bottom')
            if y <= -0.5:
                label.set_verticalalignment('top')


    def radar_factory(self,num_vars, frame='circle'):
        """Create a radar chart with `num_vars` axes.

        This function creates a RadarAxes projection and registers it.

        Parameters
        ----------
        num_vars : int
            Number of variables for radar chart.
        frame : {'circle' | 'polygon'}
            Shape of frame surrounding axes.

        """
        # calculate evenly-spaced axis angles
        theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

        class RadarAxes(PolarAxes):

            name = 'radar'

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # rotate plot such that the first axis is at the top
                self.set_theta_zero_location('N')

            def fill(self, *args, closed=True, **kwargs):
                """Override fill so that line is closed by default"""
                return super().fill(closed=closed, *args, **kwargs)

            def plot(self, *args, **kwargs):
                """Override plot so that line is closed by default"""
                lines = super().plot(*args, **kwargs)
                for line in lines:
                    self._close_line(line)

            def _close_line(self, line):
                x, y = line.get_data()
                # FIXME: markers at x[0], y[0] get doubled-up
                if x[0] != x[-1]:
                    x = np.concatenate((x, [x[0]]))
                    y = np.concatenate((y, [y[0]]))
                    line.set_data(x, y)

            def set_varlabels(self, labels):
                self.set_thetagrids(np.degrees(theta), labels)

            def _gen_axes_patch(self):
                # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
                # in axes coordinates.
                if frame == 'circle':
                    return Circle((0.5, 0.5), 0.5)
                elif frame == 'polygon':
                    return RegularPolygon((0.5, 0.5), num_vars,
                                        radius=.5, edgecolor="k")
                else:
                    raise ValueError("unknown value for 'frame': %s" % frame)

            def draw(self, renderer):
                """ Draw. If frame is polygon, make gridlines polygon-shaped """
                if frame == 'polygon':
                    gridlines = self.yaxis.get_gridlines()
                    for gl in gridlines:
                        gl.get_path()._interpolation_steps = num_vars
                super().draw(renderer)


            def _gen_axes_spines(self):
                if frame == 'circle':
                    return super()._gen_axes_spines()
                elif frame == 'polygon':
                    # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                    spine = Spine(axes=self,
                                spine_type='circle',
                                path=Path.unit_regular_polygon(num_vars))
                    # unit_regular_polygon gives a polygon of radius 1 centered at
                    # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                    # 0.5) in axes coordinates.
                    spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                        + self.transAxes)


                    return {'polar': spine}
                else:
                    raise ValueError("unknown value for 'frame': %s" % frame)

        register_projection(RadarAxes)
        return theta
    
    def getFivePowerPlot(self,heart,fight,vital,sex,health):
        plt.switch_backend('Agg') 
        fig=plt.figure()
        data = [[ "Heart "+str(heart), "Fight "+str(fight), "Vital "+str(vital), "Sex "+str(sex),"Health "+str(health)],
            #[ "Heart ", "Fight ", "Sex ", "Vital ","Health "],
            ('Basecase', [
                [heart/100, fight/100, vital/100, sex/100, health/100]
                ])]
    
        N = len(data[0])
        theta = self.radar_factory(N, frame='polygon')
        
        spoke_labels = data.pop(0)
        title, case_data = data[0]
        
        fig, ax = plt.subplots(figsize=(14,10), subplot_kw=dict(projection='radar'))
        fig.subplots_adjust(top=0.85, bottom=0.05)
        
        
        
        #ax.set_title(title,  position=(0.5, 1.1), ha='center')
        
        for d in case_data:
            line = ax.plot(theta, d)
            ax.fill(theta, d,  alpha=0.25)
        ax.set_varlabels(spoke_labels)
        ax.set_yticklabels([])
        
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8,1])
        ax.set_rmax(1)
        
        self.realign_polar_xticks(ax)
        plt.xticks(fontsize=30)
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        plot_data = buffer.getvalue()
        #buffer.seek(0)  # rewind to beginning of file
        #plot_data = base64.b64encode(buffer.getvalue())
        return plot_data

    def getTaiChiPlot(self,ratio,age):
        plt.switch_backend('Agg') 
        fig=plt.figure(figsize=(14,14))


        #新增Figure的軸（左,下,寬度,高度)，範圍佔Figure的比例（數值介於0-1）
        axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        #make background of taichi
     
        colormap=['#f7797d','#F8977f','#FAA580','#FBD786','#E5D786','#C6FF86','#C6FFB0','#C6FFDD']
        r=8
        x0=0
        y0=0
        theta=range(0,360)
        for j in range(r-1, 0, -1):
            x=[]
            y=[]
            for i in range(len(theta)):
                x.append(x0+j*math.cos(theta[i]/180*math.pi))
                y.append(y0+j*math.sin(theta[i]/180*math.pi))
            axes.fill(x,y,colormap[j])
            #plt.hold


        if age>= 80:
            radius_cali=0.5
        elif age<=18:
            radius_cali=8
        else:
            radius_cali=(7/60)*(79-age)

        outradius=radius_cali
        
        insideradius2=outradius*ratio
        insideradius1=outradius-insideradius2

        x=[]
        y=np.linspace(-outradius,outradius)
        for i in range(len(y)):
            x.append(math.sqrt(outradius**2-y[i]**2))
        axes.fill(x,y,'k')
        #plt.hold
        axes.plot(x,y,'w')

        for i in range(len(x)):
            x[i]=-x[i]
        axes.fill(x,y,'w')
        #plt.hold
        axes.plot(x,y,'w')

        x=[]
        y=np.linspace(-outradius,-outradius+2*insideradius1)
        for i in range(len(y)):
            x.append((math.sqrt(round(insideradius1**2-(y[i]+(outradius-insideradius1))**2,4))))
        axes.fill(x,y,'w')
        x=np.zeros(len(x)-4)
        axes.plot(x,y[2:len(y)-2],'w')

        x=[]
        y=np.linspace(-(2*insideradius2-outradius),outradius)
        for i in range(len(y)):
            x.append(-math.sqrt(round(insideradius2**2-(y[i]-(outradius-insideradius2))**2,4)))
        axes.fill(x,y,'k')
        x=np.zeros(len(x)-4)
        axes.plot(x,y[2:len(y)-2],'k')

        x=[]
        y=[]
        for i in range(0,360):
            x.append(x0+outradius*math.cos(theta[i]/180*math.pi))
            y.append(y0+outradius*math.sin(theta[i]/180*math.pi))

        axes.plot(x,y,'k',linewidth=5)
        #plt.hold
        #ax = plt.gca()
        axes.axis('equal')

        axes.axis('off')
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        plot_data = buffer.getvalue()

        #buffer.seek(0)  # rewind to beginning of file
        #plot_data = base64.b64encode(buffer.getvalue())
        return plot_data
