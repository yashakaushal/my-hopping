
# Writing hops to a text file

import matplotlib
import matplotlib.pyplot as plt, mpld3 
from mpld3 import plugins
from mpld3 import utils
import json 
import numpy as np
import pandas as pd

#reading catalog and dropping nan values
star_cat = pd.read_csv("/Users/yashakaushal/Documents/summer_project/data_webscraping.csv")
star_cat = star_cat.dropna(subset=["spect","mag"])

#reading columns
ra = star_cat["rarad"]
dec = star_cat["decrad"]
spect = star_cat["spect"]
mag = star_cat["mag"]
flux = 10**(-mag/2.5)

#defining spectral cuts
omask = spect.str.startswith('O')
bmask = spect.str.startswith('B')
fmask = spect.str.startswith('F')
mmask = spect.str.startswith('M')


# Write text to file on click
class ClickInfo(plugins.PluginBase):
    """Plugin for getting info on click"""

    
    JAVASCRIPT = """
    mpld3.register_plugin("clickinfo", ClickInfo);
    ClickInfo.prototype = Object.create(mpld3.Plugin.prototype);
    ClickInfo.prototype.constructor = ClickInfo;
    ClickInfo.prototype.requiredProps = ["id"];
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
    
    // 1. Create Target Input button
    var button = document.createElement("button");
    button.innerHTML = "Enter Target";

    // 2. Append somewhere
    var body = document.getElementsByTagName("body")[0];
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
      //saveAs(blob, filename)
      
    });
    
    // function to write to a text file
    function writeTextFile(afilename, output){
      var txtFile = new File(afilename);
      txtFile.writeln(output);
      txtFile.close();
    }
              
    ClickInfo.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);
        obj.elements().on("mousedown",
                          function(d, i){hops_list=hops_list+ "  " +d ; console.log(hops_list);}
                          );
                           
    }
    """
    
    def __init__(self, points):
        self.dict_ = {"type": "clickinfo",
                      "id": utils.get_id(points)}
        

fig, ax = plt.subplots(figsize=(20,12))
points = ax.scatter(ra[omask],dec[omask],s=1e4*flux[omask],color="white")
labels = ["[RA {0:.5f} \v DEC {1:.5f} \v Constellation {0:5f}]".format(i,j,k,'.2f','.2f','.2f') for i,j,k in zip(ra[omask],dec[omask],flux[omask])]
tooltip = plugins.PointLabelTooltip(points, labels)
plugins.connect(fig, tooltip)
plugins.connect(fig, ClickInfo(points))

ax.set_facecolor('midnightblue')
ax.grid(alpha=0.3)
ax.set_xlabel("RA", size =20)
ax.set_ylabel("DEC", size =20)
#plt.savefig("test1.png")

mpld3.show()
