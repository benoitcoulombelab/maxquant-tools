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
sbatch --cpus-per-task=$raws --mem=$mem maxquant.sh
```

`$raws` is the number of raw files in your dataset. If you have more than 40 raw files, use `40`

`$mem` should be equal to the number of raw files times 5 followed by the letter `G`. If you have more than 35 raw files, use `175G`

For a dataset with 8 raw files, the command should be

```
sbatch --cpus-per-task=8 --mem=40G maxquant.sh
```

## Download results

Once you receive an email telling you that MaxQuant completed, you can download the results from the following folders under `scratch/$dataset_name`

1. `combined/txt`
2. `combined/andromeda`

Use the same FTP program to download as for uploading, see [upload](upload.md)
