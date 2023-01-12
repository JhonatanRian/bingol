class PdfGenerator{imagesCount=20;padding=20;imagesPaddingTop=90;textPaddingTop=40;titleFontSize=30;cellWidth=null;cellHeight=40;cellFontSize=30;tablePaddingTop=220;tablePaddingTopWithoutTitle=50;tablePaddingBottom=80;drawColor=0;cardsPerPage=4;titleImgWidth=300;titleImgHeight=36;pageWidthDefault=595.28;pageHeightDefault=841.89;pageWidth=null;pageHeight=null;columnToLetter={0:'B',1:'I',2:'N',3:'G',4:'O'};imagesSize={4:{countPerPage:4,width:267,height:267*1.089,pdfOrientation:'p',},2:{countPerPage:2,width:392,height:392*1.089,pdfOrientation:'l',},1:{countPerPage:1,width:555,height:555*1.089,pdfOrientation:'p',},};pdfTitleImage=null;pdfTitleImageSrc='/wp-content/themes/betheme-child/bingo_generator/images/pdf-title.png'
facebookImage=null;facebookImageSrc='/wp-content/themes/betheme-child/bingo_generator/images/facebook-icon.png';instagramImage=null;instagramImageSrc='/wp-content/themes/betheme-child/bingo_generator/images/instagram-icon.png';pinterestImage=null;pinterestImageSrc='/wp-content/themes/betheme-child/bingo_generator/images/pinterest-icon.png';cardGenerator=null;setCardsPerPage(cardsPerPage){this.cardsPerPage=cardsPerPage};getImagesSize(){return this.imagesSize[this.cardsPerPage]};async showLoading(){return new Promise(function(resolve,reject){jQuery('#generator-result #pdf-loading').show();jQuery('#generate-pdf').hide();setTimeout(()=>resolve('Done'),50)})};removeLoading(){jQuery('#generator-result #pdf-loading').hide();jQuery('#generate-pdf').show()};async generatePdf(){await this.showLoading();let currentImagesSize=this.getImagesSize();const doc=new window.jspdf.jsPDF(currentImagesSize.pdfOrientation,'pt','a4',!0);if(currentImagesSize.pdfOrientation==='l'){this.pageWidth=this.pageHeightDefault;this.pageHeight=this.pageWidthDefault}
if(currentImagesSize.pdfOrientation==='p'){this.pageWidth=this.pageWidthDefault;this.pageHeight=this.pageHeightDefault}
doc.setDrawColor(this.drawColor);doc.setFont('DaxCondensedMedium','normal');this.drawTitleFooter(doc);let tableWords=this.cardGenerator.getWords();this.cellWidth=(this.pageWidth-this.padding*2)/tableWords.length;let maxTableHeight=this.pageHeight-this.tablePaddingTop-this.tablePaddingBottom;let tableHeight=tableWords[0].length*this.cellHeight;let rowsAmount=tableWords[0].length;if(tableHeight>maxTableHeight){rowsAmount=Math.floor(maxTableHeight/this.cellHeight)}
for(let i=0;i<tableWords[0].length;i+=rowsAmount){this.drawNumbersTable(doc,tableWords,rowsAmount,i);doc.addPage();this.drawTitleFooter(doc)}
let words=JSON.parse(JSON.stringify(this.cardGenerator.getWords()));for(let i=0;i<this.imagesCount;i+=currentImagesSize.countPerPage){for(let j=0;j<currentImagesSize.countPerPage;j++){this.cardGenerator.generateBingoCard(!0,!0,!0);let paddingTop=this.imagesPaddingTop;if(j>1){paddingTop=this.imagesPaddingTop+currentImagesSize.height+this.padding}
doc.addImage(this.cardGenerator.canvas,'JPEG',this.padding+(currentImagesSize.width+this.padding)*(j%2),paddingTop,currentImagesSize.width,currentImagesSize.height)}
if(i<this.imagesCount-currentImagesSize.countPerPage){doc.addPage();this.drawTitleFooter(doc)}}
this.cardGenerator.setWords(words);this.cardGenerator.generateBingoCard();doc.save(title+'.pdf',{returnPromise:!0}).then(()=>{this.removeLoading()})};drawNumbersTable(doc,words,rowsAmount,fromRow=0){doc.setFontSize(14);doc.text('Keep track of your calls with your own custom Bingo Caller’s Card! All you need\n'+'to do is print two copies of your Caller’s Card and cut the squares out of one copy.\n'+'Fold the squares in half so that you can’t see the numbers or words and then\n'+'put them in a bowl. Have the caller pull each square out of the bowl and call it\n'+'out loud when it\'s time to play bingo. Once the number or word has been called,\n'+'you can check it off the second copy of your Caller’s Card. It’s as easy as that!\n'+'Then you can always check that any called Bingo wins are valid with your second card!',this.pageWidth/2,100,{align:'center'});doc.setLineWidth(2);for(let i=0;i<this.cardGenerator.getGridSize();i++){for(let j=fromRow;j<rowsAmount+fromRow&&j<words[i].length;j++){let x=this.padding+(this.cellWidth*i);let y=this.tablePaddingTop+(this.cellHeight*(j-fromRow));doc.rect(x,y,this.cellWidth,this.cellHeight);let fontSize=this.cellFontSize;doc.setFontSize(fontSize);while(doc.compatAPI().splitTextToSize(this.columnToLetter[i]+' '+words[i][j].toString(),this.cellWidth).length>1){doc.setFontSize(--fontSize)}
doc.text(this.columnToLetter[i]+' '+words[i][j].toString(),x+this.cellWidth/2,y+this.cellHeight/2,{align:'center',maxWidth:this.cellWidth,baseline:'middle'})}}};drawTitleFooter(doc){doc.addImage(this.pdfTitleImage,'JPEG',(this.pageWidth-this.titleImgWidth)/2,30,this.titleImgWidth,this.titleImgHeight);doc.setFontSize(14);doc.text('Want to SHARE your Custom Bingo Cards? Click below!',this.pageWidth/2,this.pageHeight-65,{align:'center'});doc.addImage(this.facebookImage,'JPEG',this.padding,this.pageHeight-50,20,20);doc.textWithLink('@BingoBlitz',this.padding+25,this.pageHeight-48,{baseline:'top',url:'https://www.facebook.com/bingoblitz'});doc.addImage(this.instagramImage,'JPEG',this.pageWidth/2-55,this.pageHeight-50,20,20);doc.textWithLink('@Bingo_Blitz',this.pageWidth/2-30,this.pageHeight-48,{baseline:'top',url:'https://www.instagram.com/bingo_blitz/'});doc.addImage(this.pinterestImage,'JPEG',this.pageWidth-this.padding-25-73,this.pageHeight-50,20,20);doc.textWithLink('@BB_Blitzy',this.pageWidth-this.padding-73,this.pageHeight-48,{baseline:'top',url:'https://www.pinterest.com/BB_Blitzy/'})};loadImages(){function toDataURL(img){let canvas=document.createElement('CANVAS');let ctx=canvas.getContext('2d');canvas.height=img.naturalHeight;canvas.width=img.naturalWidth;ctx.drawImage(img,0,0);return canvas.toDataURL()}
let pdfTitleImage=new Image();pdfTitleImage.src=this.pdfTitleImageSrc
pdfTitleImage.onload=()=>{this.pdfTitleImage=toDataURL(pdfTitleImage)}
let facebookImage=new Image();facebookImage.src=this.facebookImageSrc;facebookImage.onload=()=>{this.facebookImage=toDataURL(facebookImage)}
let instagramImage=new Image();instagramImage.src=this.instagramImageSrc;instagramImage.onload=()=>{this.instagramImage=toDataURL(instagramImage)}
let pinterestImage=new Image();pinterestImage.src=this.pinterestImageSrc;pinterestImage.onload=()=>{this.pinterestImage=toDataURL(pinterestImage)}};constructor(cardGenerator){this.cardGenerator=cardGenerator;this.loadImages()}}