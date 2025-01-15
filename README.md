# ai-models

**DISCLAIMER**
This project is **BETA** and will be **Experimental** for the foreseeable future.
Interfaces and functionality are likely to change, and the project itself may be scrapped.
**DO NOT** use this software in any project/software that is operational.


The `ai-models` command is used to run AI-based weather forecasting models. These models need to be installed independently.

## Usage

Although the source code `ai-models` and its plugins are available under open sources licences, some model weights may be available under a different licence. For example some models make their weights available under the CC-BY-NC-SA 4.0 license, which does not allow commercial use. For more informations, please check the license associated with each model on their main home page, that we link from each of the corresponding plugins.

## Prerequisites

Before using the `ai-models` command, ensure you have the following prerequisites:

- Python 3.10 (it may work with different versions, but it has been tested with 3.10 on Linux/MacOS).
- An CDS account for accessing input data (see below for more details).
- A computed with a GPU for optimal performance (strongly recommended).

## Installation

To install the `ai-models` command, run the following command:

```bash
pip install ai-models
```

## Available Models

Currently, only graphcast is supported:

```bash
pip install ai-models-graphcast
```
## Running the models

To run model, make sure it has been installed, then simply run:

```bash
ai-models <model-name>
```

Replace `<model-name>` with the name of the specific AI model you want to run.

By default, the model will be run for a 10-day lead time (240 hours)

To produce a 15 days forecast, use the `--lead-time HOURS` option:

```bash
ai-models --lead-time 360 <model-name>
```

You can change the other defaults using the available command line options, as described below.

## Performances Considerations

The AI models can run on a CPU; however, they perform significantly better on a GPU. A 10-day forecast can take several hours on a CPU but only around one minute on a modern GPU.

:warning: **We strongly recommend running these models on a computer equipped with a GPU for optimal performance.**

It you see the following message when running a model, it means that the ONNX runtime was not able to find a the CUDA libraries on your system:
> [W:onnxruntime:Default, onnxruntime_pybind_state.cc:541 CreateExecutionProviderInstance] Failed to create CUDAExecutionProvider. Please reference <https://onnxruntime.ai/docs/reference/execution-providers/CUDA-ExecutionProvider.html#requirements> to ensure all dependencies are met.

To fix this issue, we suggest that you install `ai-models` in a [conda](https://docs.conda.io/en/latest/) environment and install the CUDA libraries in that environment. For example:

```bash
conda create -n ai-models python=3.10
conda activate ai-models
conda install cudatoolkit
pip install ai-models
...
```

## Start From the CDS

You can start the models using ERA5 (ECMWF Reanalysis version 5) data for the [Copernicus Climate Data Store (CDS)](https://cds.climate.copernicus.eu/). You will need to create an account on the CDS. The data will be downloaded using the [CDS API](https://cds.climate.copernicus.eu/api-how-to).

To access the CDS, simply add `--input cds` on the command line. Please note that ERA5 data is added to the CDS with a delay, so you will also have to provide a date with `--date YYYYMMDD`.

```bash
ai-models --download-assets --input cds --date 20230110 --time 0000 <model-name>
```

## Output

By default, the model output will be written in GRIB format in a file called `<model-name>.grib`. You can change the file name with the option `--path <file-name>`. If the path you specify contains placeholders between `{` and `}`, multiple files will be created based on the [eccodes](https://confluence.ecmwf.int/display/ECC) keys. For example:

```bash
 ai-models --path 'out-{step}.grib' <model-name>
 ```
To plot the data, use plot_graphcast.py.

```bash
 python3 plot_graphcast.py
 ```
