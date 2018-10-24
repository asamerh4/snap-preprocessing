#!/usr/bin/python
import os, sys, argparse, time, shutil
from subprocess import call
from subprocess import check_output

#WORK DIR is where this file resides
root_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(root_path)

#INTERNAL VARS
snapBundlePath=root_path+"/tools/snap-bundle/"
input_path=root_path+"/input"
output_path=root_path+"/output"

noDataValue=""

#RUNTIME VARS
InputProduct = os.environ['INPUT_PRODUCT']
SnapOutputProduct = os.environ['OUTPUT_PRODUCT']
warpInputFileList=[]



def projectSelectedBands():
    with open('s1-calibration.xml.template', 'r') as graph_file_template:
        graph = graph_file_template.read().format(
          manifest=input_path+"/"+InputProduct,
          snap_output=output_path+"/"+InputProduct
        )

    with open('s1-calibration.xml', 'w') as graph_file:
        graph_file.write(graph)

    snapCall='''java -cp "{snapBundlePath}*" \
      -Dsnap.mainClass="org.esa.snap.core.gpf.main.GPT" \
      -Djava.library.path="{snapBundlePath}" \
      -Dsnap.home="{snapBundlePath}" \
      -Xmx4G org.esa.snap.runtime.Launcher \
      {graph}'''.format(
        snapBundlePath=snapBundlePath,
        graph="s1-calibration.xml"
        )
        #TODO: exception handling (check_call)
    print snapCall
    call(snapCall, shell=True)

    for file in os.listdir(output_path):
        if file.endswith(".tif"):
            warpInputFileList.append(file)
    return warpInputFileList


def WarpToUTM(warpInputFileList):
    for inFile in warpInputFileList:
        warp = '''gdalwarp -overwrite -tr 100 100 \
              -t_srs "EPSG:32633" \
              {inFile} \
              {outFile}'''.format(
                inFile=output_path+"/"+InputProduct+".calib.tif",
                outFile=output_path+"/"+inFile+".calib-utm.tif"
                )
        #TODO: exception handling (check_call)
        call(warp, shell=True)

# def syncToS3AndRegister(tiles, productInfo):
    # s3UploadCall='''aws --endpoint-url https://obs.eu-de.otc.t-systems.com \
      # s3 sync tiles/ {s3OutputProductPrefix}'''.format(
        # s3OutputProductPrefix=s3OutputProductPrefix
        # )
    # call(s3UploadCall, shell=True)

    # s3RegisterCall='''aws --endpoint-url https://obs.eu-de.otc.t-systems.com \
      # s3 cp {xfdu} {s3OutputProductPrefix}products/{productName}/'''.format(
        # s3OutputProductPrefix=s3OutputProductPrefix,
        # productName=productInfo[0],
        # xfdu=productInfo[1]
        # )
    # call(s3RegisterCall, shell=True)

# def cleanup():
    # shutil.rmtree("s3product")
    # shutil.rmtree("snap_output")
    # shutil.rmtree("tiles")

def main():
    print "\n====================================="
    print "sentinel-1 calibration & product to utm"
    print "======================================="
    #run snap
    print "\n**PROJECT selected bands using snap"
    warpInputFileList = projectSelectedBands()

    #run gdalwarp
    print "\n**run GDALWARP..."
    WarpToUTM(warpInputFileList)
    #Upload/Sync and Register
    # syncToS3AndRegister(tiles, productInfo)
    # cleanup()

if __name__ == "__main__":
    main()
