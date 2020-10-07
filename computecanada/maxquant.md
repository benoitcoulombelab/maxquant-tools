# MaxQuant

:information_source: *[Connecting to Compute Canada server](connect.md)*

#### Steps

* [Upload dataset files to Compute Canada](#upload-dataset-files-to-compute-canada)
* [Run MaxQuant](#run-maxquant)
* [Download results](#download-results)

## Upload dataset files to Compute Canada

See [Uploading dataset files to Compute Canada server](upload.md)

## Run MaxQuant

Run the following command

```
maxquant
```

This will add a job to run MaxQuant using `sbatch` with 1 CPU and 5 GB of memory per sample.

## Download results

Once you receive an email telling you that MaxQuant completed, you can download the results from the following folders under `scratch/$dataset_name`

1. `combined/txt`
2. `combined/andromeda`

Use the same FTP program to download as for uploading, see [upload](upload.md)
