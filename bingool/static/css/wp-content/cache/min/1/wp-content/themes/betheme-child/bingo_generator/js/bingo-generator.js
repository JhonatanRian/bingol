(function($){let templates=[{groupName:'Celebrations',values:[{title:'Bingo',optionValue:'Bingo',imgUrl:'celebrations/bingo_generic.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Birthday',optionValue:'Birthday',imgUrl:'celebrations/birthday.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Family/friends BBQ',optionValue:'Family-friends-BBQ',imgUrl:'celebrations/bbq.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Family reunions',optionValue:'Family-reunions',imgUrl:'celebrations/family_reunion.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Bachelorette party',optionValue:'Bachelorette-party',imgUrl:'celebrations/bachelorette_party.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Baby shower',optionValue:'Baby-shower',imgUrl:'celebrations/baby_shower.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},],},{groupName:'Holidays',values:[{title:'4th July',optionValue:'default',imgUrl:'holidays/july_4th.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Christmas eve',optionValue:'christmas-eve',imgUrl:'holidays/christmas.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Easter',optionValue:'easter',imgUrl:'holidays/easter.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'New Year',optionValue:'new-year',imgUrl:'holidays/new_years_eve.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Valentine\'s day',optionValue:'valentines-day',imgUrl:'holidays/valentine.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Halloween',optionValue:'halloween',imgUrl:'holidays/halloween.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Summer',optionValue:'summer',imgUrl:'holidays/summer.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},],},{groupName:'Cities',values:[{title:'New-York',optionValue:'New-York',imgUrl:'cities/new_york.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Madrid',optionValue:'Madrid',imgUrl:'cities/madrid.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Tokyo',optionValue:'Tokyo',imgUrl:'cities/tokyo.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Paris',optionValue:'Paris',imgUrl:'cities/paris.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'London',optionValue:'London',imgUrl:'cities/london.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:45,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},{title:'Hong Kong',optionValue:'HongKong',imgUrl:'cities/hong_kong.png',color:'#0b0b0b',fontSize:60,fontFamily:'DaxCondensed',titleFontSize:50,titleFontFamily:'DaxCondensed',titleColor:'#000',bgColor:'#fff9b0',},],},];$(document).ready(function(){let textToSpeech=new TextToSpeech();let cardGenerator=new CardGenerator();cardGenerator.createTemplatesPopup(templates);cardGenerator.createGridSizeSelect();cardGenerator.createTitleInput();cardGenerator.createGridInputs();cardGenerator.generateBingoCard();let pdfGenerator=new PdfGenerator(cardGenerator);$('#generate-pdf').click((e)=>{e.preventDefault();pdfGenerator.generatePdf()});$('input[name="cards-per-page"]').change(function(){pdfGenerator.setCardsPerPage(this.value)});let bingoCaller=new BingoCaller(textToSpeech);$('#play-now').click(function(e){e.preventDefault();if($('#play-now').data('is-started')==='true'){bingoCaller.stop.call(bingoCaller)}else{bingoCaller.start.call(bingoCaller,cardGenerator.getWords())}});addEventListener('gridInputWasChanged',function(e){bingoCaller.stop();textToSpeech.speak(e.detail.word)});addEventListener('gridSizeWasChanged',function(e){bingoCaller.stop()})})})(jQuery)