#!/bin/bash

THREADS=`getconf _NPROCESSORS_ONLN`
BUILDBLOCKS_LOG="/tmp/buildblocks.log"

echo -----------------------------------------------------------
echo ----------------------- Cleaning up -----------------------
echo -----------------------------------------------------------

rm -rf ~/.grc_gnuradio/*
chmod +x results_cleanup.sh
./results_cleanup.sh

echo -----------------------------------------------------------
echo -------------- Installing FrameworkCRN --------------------
echo -----------------------------------------------------------
cd gr-pmt_cpp/
mkdir build
cd build/
cmake ../
make -j$THREADS && \
sudo make install
sudo ldconfig
cd ..
cd ..

sudo mkdir -p /opt/FrameworkCRN
sudo cp gr-pmt_cpp/python/final_data_config3.net /opt/FrameworkCRN/final_data_config.net
sudo chown -R root.users /opt/FrameworkCRN
sudo chmod -R 0755 /opt/FrameworkCRN

echo -----------------------------------------------------------
echo -------------- Building FrameworkCRN Blocks ---------------
echo -----------------------------------------------------------
echo "Building: dependencies/gr-ieee802-15-4/examples/ieee802_15_4_OQPSK_PHY.grc"
if ! bash -c 'grcc dependencies/gr-ieee802-15-4/examples/ieee802_15_4_OQPSK_PHY.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building ieee802_15_4_OQPSK_PHY.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/get_power.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/get_power.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building get_power.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/file_recorder.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/file_recorder.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building file_recorder.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/802.15.4_Cog.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/802.15.4_Cog.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building 802.15.4_Cog.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/sbrc17/mobility_master.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/sbrc17/mobility_master.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building mobility_master.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/sbrc17/share_master.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/sbrc17/share_master.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building share_master.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/sbrc17/decision.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/sbrc17/decision.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building decision.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/sbrc17/sense_master.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/sbrc17/sense_master.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building sense_master.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/sbrc17/usrp.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/sbrc17/usrp.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building usrp.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/sbrc17/usrp_master.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/sbrc17/usrp_master.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building usrp_master.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/sbrc17/mobility.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/sbrc17/mobility.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building mobility.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/sbrc17/sense.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/sbrc17/sense.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building sense.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/sbrc17/send_data_sense.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/sbrc17/send_data_sense.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building send_data_sense.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/sbrc17/share.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/sbrc17/share.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building share.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/sbrc17/slave.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/sbrc17/slave.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building slave.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

echo "Building: gr-pmt_cpp/grc/sbrc17/master.grc"
if ! bash -c 'grcc gr-pmt_cpp/grc/sbrc17/master.grc' 2>&1 >> $BUILDBLOCKS_LOG ; then
	echo "Error building master.grc... check $BUILDBLOCKS_LOG for detailed information"
	exit 1
fi

ln -sf gr-pmt_cpp/grc/master.grc ./master.grc
ln -sf gr-pmt_cpp/grc/slave.grc ./slave.grc

echo -----------------------------------------------------------
echo ---------- FrameworkCRN Installed Successfully ------------
echo -----------------------------------------------------------
