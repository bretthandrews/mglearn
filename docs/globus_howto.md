# Globus How To

[Getting Started](https://docs.globus.org/how-to/get-started/)

[Downloading SDSS data](https://trac.sdss.org/wiki/DataArchive/DataTransfer#GlobusTransfers)

SDSS Endpoints:
- `sdss#public`
- `SDSS Collab`

[How to setup laptop as Globus endpoint](https://www.globus.org/globus-connect)


## Globus CLI

[Globus CLI Installation Walk Through](https://docs.globus.org/cli/installation/)
[Globus CLI Usage](https://docs.globus.org/cli/using-the-cli/)

1. Install Globus:
  * `pip install globus-cli`
2. Login:
  * `globus login`
3. Use [web app](https://www.globus.org/app/transfer) to login to "SDSS Collab" endpoint with Utah unid account.
4. Get ID of "SDSS Collab" endpoint:
  * `globus endpoint search "SDSS Collab"`
5. Set shell variable name for the SDSS Collab endpoint ID:
  * `ep1=d5990424-6d04-11e5-ba46-22000b92c6ec`
6. Get ID of local endpoint [REPLACE "jaqen" with your local endpoint]:
  * `globus endpoint search 'jaqen'`
7. Set shell variable name for local endpoint ID [REPLACE "e3b42860-3b33-11e7-bcf7-22000b9a448b" with your local endpoint's ID]:
  * `ep2=e3b42860-3b33-11e7-bcf7-22000b9a448b`
8. Transfer files (modify path to text file as needed):
  * Cubes: `globus transfer $ep1:/uufs/chpc.utah.edu/common/home/sdss/mangawork/manga/spectro/ $ep2:~/projects/sdss/sas/mangawork/manga/spectro/ --batch --label "Cubes Batch" < ~/projects/mangaML/data/samples/mpl5_main_sample_LOGCUBE.txt`
  * RSS: `globus transfer $ep1:/uufs/chpc.utah.edu/common/home/sdss/mangawork/manga/spectro/ $ep2:~/projects/sdss/sas/mangawork/manga/spectro/ --batch --label "RSS Batch" < ~/projects/mangaML/data/samples/mpl5_main_sample_LOGRSS.txt`
  * Images: `globus transfer $ep1:/uufs/chpc.utah.edu/common/home/sdss/mangawork/manga/spectro/ $ep2:~/projects/sdss/sas/mangawork/manga/spectro/ --batch --label "Images Batch" < ~/projects/mangaML/data/samples/mpl5_main_sample_images.txt`
  * Maps: `globus transfer $ep1:/uufs/chpc.utah.edu/common/home/sdss/mangawork/manga/spectro/ $ep2:~/projects/sdss/sas/mangawork/manga/spectro/ --batch --label "Maps Batch" < ~/projects/mangaML/data/samples/mpl5_main_sample_maps.txt`
9. [Check transfer status](https://www.globus.org/app/activity/)

