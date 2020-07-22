import matplotlib
import matplotlib.pyplot as plt, mpld3 
import pandas as pd 
from mpld3 import plugins
from mpld3 import utils
from matplotlib.patches import Circle
from svgpath2mpl import parse_path
import matplotlib.lines as mlines
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

ng = pd.read_csv('/Users/yashakaushal/Documents/summer_project/interface/NGC.csv')
ms = pd.read_csv('/Users/yashakaushal/Documents/summer_project/interface/messier_objects.csv')
cb = pd.read_csv('/Users/yashakaushal/Documents/summer_project/interface/constellation_borders.csv')
ty = pd.read_csv('/Users/yashakaushal/Documents/summer_project/interface/tycho_1.csv')

ga = parse_path("""M 490.60742,303.18917 A 276.31408,119.52378 28.9 0 1 190.94051,274.29027 276.31408,119.52378 28.9 0 1 6.8010582,36.113705 276.31408,119.52378 28.9 0 1 306.46799,65.012613 276.31408,119.52378 28.9 0 1 490.60742,303.18917 Z""")
ga.vertices -= ga.vertices.mean(axis=0)
# red

cl = parse_path("""M 541.64941,265.49102 A 270.8247,265.49102 0 0 1 270.82471,530.98205 270.8247,265.49102 0 0 1 0,265.49102 270.8247,265.49102 0 0 1 270.82471,0 270.8247,265.49102 0 0 1 541.64941,265.49102 Z""")
cl.vertices -= cl.vertices.mean(axis=0)
# yellow

pn2 = parse_path("""m 0,326.75709 v 18.09653 h 671.61069 v -18.09653 z m 326.7571,344.85359 h 18.0965 V 0 h -18.0965 z""")
pn2.vertices -= pn2.vertices.mean(axis=0)
# black

pl = parse_path("""m 65.722069,112.42727 v 2.87837 h 2.878368 v 0.87849 h -2.878368 v 2.87837 h -0.868162 v -2.87837 h -2.878368 v -0.87849 h 2.878368 v -2.87837 z""")
pl.vertices -= pl.vertices.mean(axis=0)      

cp = parse_path("""M 749.48177,361.96144 V 387.5203 H 0 V 361.96144 Z M 361.96144,0 h 25.55886 v 749.48177 h -25.55886 z m 239.5511,374.74089 A 226.77166,226.77166 0 0 1 374.74089,601.51254 226.77166,226.77166 0 0 1 147.96923,374.74089 226.77166,226.77166 0 0 1 374.74089,147.96923 226.77166,226.77166 0 0 1 601.51254,374.74089 Z""")
cp.vertices -= cp.vertices.mean(axis=0)  

pn4 = parse_path("""M 488,240 H 256 V 8 c 0,-4.418 -3.582,-8 -8,-8 -4.418,0 -8,3.582 -8,8 V 240 H 8 c -4.418,0 -8,3.582 -8,8 0,4.418 3.582,8 8,8 h 232 v 232 c 0,4.418 3.582,8 8,8 4.418,0 8,-3.582 8,-8 V 256 h 232 c 4.418,0 8,-3.582 8,-8 0,-4.418 -3.582,-8 -8,-8 z""")
pn4.vertices -= pn4.vertices.mean(axis=0)

tfile = open('/Users/yashakaushal/Documents/summer_project/interface/target.txt', 'r')
ttext = tfile.read()  
#if ttext
    
# Editor Interface

class ClickInfo(plugins.PluginBase):
    """Plugin for getting info on click"""

    
    JAVASCRIPT = """
    mpld3.register_plugin("clickinfo", ClickInfo);
    ClickInfo.prototype = Object.create(mpld3.Plugin.prototype);
    ClickInfo.prototype.constructor = ClickInfo;
    ClickInfo.prototype.requiredProps = ["id"];
    ClickInfo.prototype.defaultProps = {labels:null};

    function ClickInfo(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };
    
    // Function to download the contents
    function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
    }
    
    var hops_list = "" ;
    var target = "";
    
    // 1. Create Save button
    var button = document.createElement("button");
    button.innerHTML = "Save Hops";

    // 2. Append somewhere
    var body = document.getElementsByTagName("body")[0];
    body.appendChild(button);

    // 3. Add event handler
    button.addEventListener ("click", function() {
      download(hops_list, 'hops.txt', 'text/plain')
      alert("Downloaded Hops");
    });
    
    // 1. Create Undo button
    var button = document.createElement("button");
    button.innerHTML = "Undo";

    // 2. Append somewhere
    var body = document.getElementsByTagName("body")[0];
    body.appendChild(button);

    // 3. Add event handler
    button.addEventListener ("click", function() {
      var str = hops_list.slice(0,-39);
      hops_list = str;
      alert("One Hop-Click Deleted");
    });
    
    // 1. Create User Input button
    var button = document.createElement("button");
    button.innerHTML = "Enter Target";

    // 2. Append somewhere
    var body = document.getElementsByTagName("body")[0];
    body.style.right = "300px"
    body.appendChild(button);

    // 3. Add event handler
    button.addEventListener ("click", function() {
      var object = window.prompt("Enter the name of target object: ");
      target = target + " " + object;
      download(target, 'target.txt', 'text/plain')
      var filename = "target.txt"
      var blob = new Blob([target], {
       type: "text/plain;charset=utf-8"
      });
      
    });
    
    // function to write to a text file
    function writeTextFile(afilename, output){
      var txtFile = new File(afilename);
      txtFile.writeln(output);
      txtFile.close();
    }
    
    ClickInfo.prototype.draw = function(){
        for(var i=0; i<this.props.id.length; i++){
            var obj = {};
            obj.label = this.props.labels[i];
            var element_id = this.props.id[i];
            mpld3_elements = [];
            
            for(var j=0; j<this.props.id.length; j++){
                var mpld3_element = mpld3.get_element(this.props.id[j], this.fig);

                // mpld3_element might be null in case of Line2D instances
                // for we pass the id for both the line and the markers. Either
                // one might not exist on the D3 side
                if(mpld3_element){
                    mpld3_elements.push(mpld3_element);
                }
            }

            obj.mpld3_elements = mpld3_elements;
            mpld3_element.elements().on("mousedown",
                              function(d, i){hops_list=hops_list+ "  " +d ; console.log(hops_list);
                                              alert("Hop-Stored")}
                              );
        }                   
    }  
    """
    
    def __init__(self, p, l):
        self.dict_ = {"type": "clickinfo",
                      "id": [utils.get_id(i) for i in p],
                      "labels": l}
        print([utils.get_id(i) for i in p])
        

def func2(ra,dec,mag,fov):
    
# sorting objects under the user input of limiting magnitude; 
# also duplicating the the objects and transforming them so they are repeated to the left of y-axis
    mag_ng = ng[(ng["mag"]<=mag)]
    mag_ms = ms[(ms['V']<=mag)]
    mag_ty = ty[(ty['V']<=mag)]
    dup_ng =  mag_ng.copy(deep=True)
    dup_ms =  mag_ms.copy(deep=True)
    dup_ty =  mag_ty.copy(deep=True)
    dup_ng['_RAJ2000'] -= 360
    dup_ms['RAJ2000'] -= 360 
    dup_ty['_RAJ2000'] -= 360 
    
# breathing space aroung the fov circle in the plot
    xl = ra-fov/2-fov/10 
    xr = ra+fov/2+fov/10
    yb = dec-fov/2-fov/10
    yt = dec+fov/2+fov/10
    
    fig, ax = plt.subplots(figsize=(17,12))
#     ax.set_aspect('equal')

#     ax.set_xlim([xl,xr])
#     ax.set_ylim([yb,yt])

    ax.set_yticklabels([round(y,2) for y in ax.get_yticks()])
    ax.set_xticklabels([(x+360) if x<0 else round(x,2) for x in ax.get_xticks()])
    
    ax.set_xlabel('Right Ascension (degrees)', fontsize=20)
    ax.set_ylabel('Declination (degrees)', fontsize=20)

# sorting objects in messier_objects.csv according to objects
    cl_ms = ms[(ms["OTYPE_3"]=='OpC')|(ms["OTYPE_3"]=='GlC')|(ms["OTYPE_3"]=='Cl*')]
    pn_ms = ms[(ms["OTYPE_3"]=='PN')]
    ga_ms = ms[(ms["OTYPE_3"]=='G')|(ms["OTYPE_3"]=='Sy2')|(ms["OTYPE_3"]=='IG')|(ms["OTYPE_3"]=='GiG')|(ms["OTYPE_3"]=='GiP')|(ms["OTYPE_3"]=='SyG')|(ms["OTYPE_3"]=='SBG')|(ms["OTYPE_3"]=='BiC')|(ms["OTYPE_3"]=='H2G')]
    re_ms = ms[(ms["OTYPE_3"]=='HII')|(ms["OTYPE_3"]=='As*')|(ms["OTYPE_3"]=='LIN')|(ms["OTYPE_3"]=='mul')|(ms["OTYPE_3"]=='RNe')|(ms["OTYPE_3"]=='AGN')]
# duplicated data sort by object type
    dup_cl_ms = dup_ms[(dup_ms["OTYPE_3"]=='OpC')|(dup_ms["OTYPE_3"]=='GlC')|(dup_ms["OTYPE_3"]=='Cl*')]
    dup_pn_ms = dup_ms[(dup_ms["OTYPE_3"]=='PN')]
    dup_ga_ms = dup_ms[(dup_ms["OTYPE_3"]=='G')|(dup_ms["OTYPE_3"]=='Sy2')|(dup_ms["OTYPE_3"]=='IG')|(dup_ms["OTYPE_3"]=='GiG')|(dup_ms["OTYPE_3"]=='GiP')|(dup_ms["OTYPE_3"]=='SyG')|(ms["OTYPE_3"]=='SBG')|(dup_ms["OTYPE_3"]=='BiC')|(dup_ms["OTYPE_3"]=='H2G')]
    dup_re_ms = dup_ms[(dup_ms["OTYPE_3"]=='HII')|(dup_ms["OTYPE_3"]=='As*')|(dup_ms["OTYPE_3"]=='LIN')|(dup_ms["OTYPE_3"]=='mul')|(dup_ms["OTYPE_3"]=='RNe')|(dup_ms["OTYPE_3"]=='AGN')]
       
    print(f"Observing RA: {ra} deg, DEC: {dec} deg, FoV: {fov} deg, Limiting Magnitude: {mag}") 
    
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major',alpha=0.3)
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    ax.set_facecolor('midnightblue')
    
# if user input ra is nearer to 360 deg, the region near 0 is plotted; here the duplicated and transformed data from above is useful
    if xr>360:
        ra-=360  
        xr-=360
        xl-=360

# scatter messier
    p1 = ax.scatter(cl_ms['RAJ2000'],cl_ms['DEJ2000'],color='yellow',s=60,zorder=10)
    l1 = ["[RA {0:.5f} \v DEC {1:.5f} \v Constellation {2}]".format(i,j,k,'.2f','.2f','%s') for i,j,k in zip(cl_ms['RAJ2000'],cl_ms['DEJ2000'],cl_ms['Constellation'])]
    t1 = plugins.PointLabelTooltip(p1, l1)
    plugins.connect(fig, t1)

    p2 = ax.scatter(pn_ms['RAJ2000'],pn_ms['DEJ2000'],color='white',s=5)
    l2 = ["[RA {0:.5f} \v DEC {1:.5f} \v Constellation {2}]".format(i,j,k,'.2f','.2f','%s') for i,j,k in zip(pn_ms['RAJ2000'],pn_ms['DEJ2000'],pn_ms['Constellation'])]
    t2 = plugins.PointLabelTooltip(p2, l2)
    plugins.connect(fig, t2)

    p3 = ax.scatter(ga_ms['RAJ2000'],ga_ms['DEJ2000'],color='red',s=60,zorder=20)
    l3 = ["[RA {0:.5f} \v DEC {1:.5f} \v Constellation {2}]".format(i,j,k,'.2f','.2f','%s') for i,j,k in zip(ga_ms['RAJ2000'],ga_ms['DEJ2000'],ga_ms['Constellation'])]
    t3 = plugins.PointLabelTooltip(p3, l3)
    plugins.connect(fig, t3)

    p4 = ax.scatter(re_ms['RAJ2000'],re_ms['DEJ2000'],c='white',s=5)
    l4 = ["[RA {0:.5f} \v DEC {1:.5f} \v Constellation {2}]".format(i,j,k,'.2f','.2f','%s') for i,j,k in zip(re_ms['RAJ2000'],re_ms['DEJ2000'],re_ms['Constellation'])]
    t4 = plugins.PointLabelTooltip(p4, l4)
    plugins.connect(fig, t4)

# scatter ngc
    p5 = ax.scatter(mag_ng['_RAJ2000'], mag_ng['_DEJ2000'], c='white',alpha=0.8,s=5)
    l5 = ["[RA {0:.5f} \v DEC {1:.5f} \v Constellation {2}]".format(i,j,k,'.2f','.2f','%s') for i,j,k in zip(mag_ng['_RAJ2000'],mag_ng['_DEJ2000'],mag_ng['Constellation'])]
    t5 = plugins.PointLabelTooltip(p5, l5)
    plugins.connect(fig, t5)

    # p6 = ax.scatter(dup_ng['_RAJ2000'], dup_ng['_DEJ2000'], c='white',alpha=0.8,s=5)
    # l6 = ["[RA {0:.5f} \v DEC {1:.5f} \v Constellation {0:5f}]".format(i,j,k,'.2f','.2f','%s') for i,j,k in zip(dup_ng['_RAJ2000'],dup_ng['_DEJ2000'],dup_ng['Constellation'])]
    # t6 = plugins.PointLabelTooltip(p6, l6)
    # plugins.connect(fig, t6)

    points = [p1,p2,p3,p4,p5]
    labels = [l1,l2,l3,l4,l5]
    plugins.connect(fig, ClickInfo(points,labels))

# constellation borders
    for i in cb['Constellation'].unique():
        x = cb[(cb['Constellation']==i)]['RAJ2000']
        y = cb[(cb['Constellation']==i)]['DEJ2000']
        x1 = x.iloc[10]
        y1 = y.iloc[10]
        ax.scatter(x,y,color='green', s=20/fov)
        ax.annotate('%s'%i, (x1,y1),size = 20)
        
        
    ax.add_artist(plt.Circle((ra, dec), fov/2, color='#00af08',zorder=-1, alpha=0.2))
    
    
    cluster = mlines.Line2D([], [], color='yellow', marker=cl, linestyle='None',
                              markersize=20, label='Clusters', markeredgecolor="black", markeredgewidth=1)
    plantary_neb = mlines.Line2D([], [], color='green', marker=cl, linestyle='None',
                              markersize=20, label='Planetory Nebula')
    planetary_neb2 = mlines.Line2D([], [], color='black', marker=pn4, linestyle='None',
                              markersize=20, label='Planetory Nebula')
    galaxy = mlines.Line2D([], [], color='Red', marker=ga, linestyle='None',
                              markersize=20, label='Galaxies')
    rest = mlines.Line2D([], [], color='white', marker=cl, linestyle='None',
                              markersize=20, label='Rest', markeredgecolor="white", markeredgewidth=1)
    plt.legend(handles=[cluster,planetary_neb2, galaxy, rest], labelspacing=5, ncol=4, borderpad=1, loc='lower center')

    mpld3.show()

func2(300,20,29,12)