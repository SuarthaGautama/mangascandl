mangascandl is a Command Line Interface (CLI) utility for downloading manga by chapter from Online manga scan reader. Currently only support mangareader.net.


##Requirements
- Python 3.x


## Installing mscandl

mangascandl is available on PyPI as pip package. To install the CLI, run:

```shell
$sudo pip install mangascandl
```


##Supported Sites


* [Mangareader](https://www.mangareader.net)
* [Mangadex](https://mangadex.org)


##mangascandl CLI Usage

To download mangascan chapter run this command:

Download by chapter:

```shell
$ mangascandl download [chapter_link] [<optional> folder name]
```


Download multiple chapter:

```shell
$ mangascandl batch [manga_page_link] [start_chapter] [end_chapter] [<optional> folder name]
```

##Example
Download mangascan by chapter:

```shell
$ mangascandl download https://www.mangareader.net/golden-kamui/3
```
Download mangascan by batch

```shell
$ mangascandl batch https://www.mangareader.net/golden-kamui/ 1 10 'Golden Kamui Vol 1'
```


for batch download, if there are folder name, the file will be downloaded in one folder
