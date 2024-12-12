FROM plattar/python-usd:version-22.05b-slim-bullseye

ENV USD_SCHEMA_FOLDER="usd_schemas"
ENV USDZCONVERT_FOLDER="usdzconvert"

WORKDIR /usr/src/app

# Update the environment path for USDZ Convert Tools
ENV USDZCONVERT_BIN_PATH="/usr/src/app/xrutils/${USDZCONVERT_FOLDER}"
ENV PATH="${PATH}:${USDZCONVERT_BIN_PATH}"

# copy source folders into container
COPY /${USD_SCHEMA_FOLDER} /usr/src/app/${USD_SCHEMA_FOLDER}
COPY /${USDZCONVERT_FOLDER} ${USDZCONVERT_BIN_PATH}
COPY FBX2glTF-linux-x64 .

RUN ln -s /usr/src/app/FBX2glTF-linux-x64 ${USDZCONVERT_BIN_PATH}/fbx2glb && \
	apt-get update && apt-get install -y --no-install-recommends \
	git \
	build-essential \
	cmake \
	nasm \
	libxrandr-dev \
	libxcursor-dev \
	libxinerama-dev \
	libxi-dev && \
	rm -rf /var/lib/apt/lists/* && \
	# Clone the USD Repository
	git clone --branch "v${USD_VERSION}" --depth 1 https://github.com/PixarAnimationStudios/USD.git usdsrc && \
	# Copy the AR Schema Components into the examples folder
	cp -a /usr/src/app/${USD_SCHEMA_FOLDER}/usdInteractive/ usdsrc/pxr/usd/ && \
	# Use usdGenSchema to Generate all CPP source files that will be built
	cd usdsrc/pxr/usd/usdInteractive && usdGenSchema schema.usda . && cd /usr/src/app && \
	# Add the directories into the CMakeLists.txt so everything gets built
	echo "add_subdirectory(usdInteractive)" >> usdsrc/pxr/usd/CMakeLists.txt && \
	# Remove the old USD installation
	rm -rf ${USD_BUILD_PATH} && \
	# build a new version with our new schemas
	python3 usdsrc/build_scripts/build_usd.py --no-examples --no-tutorials --no-imaging --no-usdview --no-draco --no-docs --no-tests ${USD_BUILD_PATH} && \
	# remove source code as we don't need it anymore
	rm -rf usdsrc && \
	rm -rf ${USD_SCHEMA_FOLDER} && \
	# remove build files we no longer need to save space
	rm -rf ${USD_BUILD_PATH}/build && \
	rm -rf ${USD_BUILD_PATH}/cmake && \
	rm -rf ${USD_BUILD_PATH}/pxrConfig.cmake && \
	rm -rf ${USD_BUILD_PATH}/share && \
	rm -rf ${USD_BUILD_PATH}/src && \
	# remove packages we no longer need/require
	# this keeps the container as small as possible
	# if others need them, they can install when extending
	apt-get purge -y git \
	build-essential \
	cmake \
	nasm \
	libxrandr-dev \
	libxcursor-dev \
	libxinerama-dev \
	libxi-dev && \
	apt autoremove -y && \
	apt-get autoclean -y
