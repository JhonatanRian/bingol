// VISIBLE AND HIDE - RODADAS ESPECIAIS

var ativo = false;

$('.home-btn-reservar').click(function(){
    if($(this).parent().parent().siblings().hasClass('active')){        
        $(this).parent().parent().siblings().removeClass('active');            
    }
    else{
        $('.home-rodadas-dropdown').removeClass('active');
        $(this).parent().parent().siblings().addClass('active');        
    }
});

$('.rodadas-btn-volta').click(function(){
    // $('.home-rodadas-dropdown').removeClass('active');
    $(this).parent().parent().parent().parent().removeClass('active'); 
});

function initGame() {
    const btnJogarGame = document.querySelector('#jogar-game');
    const contentBox = document.querySelector('.contet-rodada');
    const contentBoxBolas = document.querySelector('.content-bolas-rodada');
    const contentTabela = document.querySelector('.contet-tabela-rodada');
    const btnArrowLeft = document.querySelector('.content-bolas-rodada .arrow-right');
    const btnArrowRight = document.querySelector('.contet-tabela-rodada .arrow-left');
    const boxRodada = document.querySelector('.box-proxima-rodada > div');

    if (btnJogarGame && btnArrowLeft && btnArrowRight) {

        function initGame() {
            contentBox.classList.remove('active');
            contentBoxBolas.classList.add('active');
            btnJogarGame.remove();
        }

        function showBoxLeft() {
            contentBoxBolas.classList.remove('active');
            contentTabela.classList.add('active');
            boxRodada.classList.add('yellow');
        }

        function showBoxRight() {
            contentBoxBolas.classList.add('active');
            contentTabela.classList.remove('active');
            boxRodada.classList.remove('yellow');
        }

        btnJogarGame.addEventListener('click', initGame);
        btnArrowLeft.addEventListener('click', showBoxLeft);
        btnArrowRight.addEventListener('click', showBoxRight);
    }
}

initGame();


// function initOpenCartela() {
//     const btnCartelas = document.querySelector('.header-comprar .arrow-down');
//     const contentCartelas = document.querySelector('.comprar-cartelas .compra-cartela');
//     const infoCompra = document.querySelector('.info-compra');
//     const loop6 = document.querySelector('.loop6');
//     const loop8 = document.querySelector('.loop8');

//     if (btnCartelas) {
//         function toggleContentCartelas() {
//             // btnCartelas.querySelector('span').classList.toggle('active');
//             contentCartelas.classList.toggle('active');
//             infoCompra.classList.toggle('active');
//             loop6.classList.toggle('active');
//             loop8.classList.toggle('active');

//             // btnCartelas.innerText = '';
//         }
//         btnCartelas.addEventListener('click', toggleContentCartelas);
//     }
// }

// initOpenCartela();



// SHOW AND HIDE MENU LATERAL MOBILE 

$('.menu-icon-mobile').click(function(){
    $('.nav-mobile').addClass('active');
    $('.header-game .col-8').removeClass('active');
    $('.header .group').removeClass('active');    
});

$('.nav-mobile .close-menu').click(function(){
    $('.nav-mobile').removeClass('active');
});


$('.header-game .saldo').click(function(){
    $('.header-game .col-8').addClass('active');
    $('.nav-mobile').removeClass('active');
});

$('.header-game .close-menu').click(function(){
    $('.header-game .col-8').removeClass('active');
});


$('.header .saldo').click(function(){
    $('.header .group').addClass('active');
    $('.nav-mobile').removeClass('active');
});

$('.header .close-menu').click(function(){
    $('.header .group').removeClass('active');
});


$('.bt-deslogado').click(function(){
    $('.header .group').addClass('active');    
    $('.nav-mobile').removeClass('active');
});

$('.header .close-menu').click(function(){
    $('.nav-mobile').removeClass('active');
    $('.header .group').removeClass('active');    
});


function imprimir() {
    window.print();
}