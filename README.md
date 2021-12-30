# humble-bundle-downloader
Downloads all pdfs, epubs, or mobis from a purchased Humble Bundle. I realized one day that I had a lot of bundles purchased from Humble Bundle and that I hadn't saved them to my local hard drive/OneDrive. I wanted to save them all in multiple formats (PDF and epub). The Direct Link save feature on the Humble Bundle website isn't the best, and it was taking forever to download every book from every bundle in two different formats. I realized that the direct links to download each of the books in each format was in the HTML for each bundle's page, so I decided to scrape a locally downloaded bundle's page to then download each book in the format(s) I wanted.

Please let me know if this ends up helping you, and I welcome any pull requests/issues to make it a bit better.

## Pre-Steps
1. Most importantly, purchase book bundles from Humble Bundle
2. Go to your book library  
![Purchases button](https://github.com/andrew-kline/humble-bundle-downloader/blob/main/img/1-purchasesbutton.png?raw=true)   

3. Select the relevant bundle
![Select bundle from table](https://github.com/andrew-kline/humble-bundle-downloader/blob/main/img/2-purchases.png?raw=true)

4. While on the bundle page, select ctl+s
![ctl+s while on bundle page](https://github.com/andrew-kline/humble-bundle-downloader/blob/main/img/3-bundlepage.png?raw=true)

5. Ensure to save as a complete web page (which will give you some extra files, but the resulting lone .html file will have the correct links). Saving this to the same directory where downloader.py lives is recommended
![Download as complete webpage](https://github.com/andrew-kline/humble-bundle-downloader/blob/main/img/4-savewebpagecomplete.png?raw=true)

## Steps
1. Run downloader.py while providing the .html or .htm file(s) that was downloaded in the pre-steps
