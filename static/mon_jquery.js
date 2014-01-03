$(document).ready(function()
{
	
	
	//===== Fonction de one page site =====//
	window.onload = function()
	{
			var page_height = $(document).height();
			var header_height = $('#menu_top').height();
			var footer_height = $('footer').height();
			var corps_height = page_height - header_height - footer_height-100;
			$('.corps').css('height',corps_height);
	}
	//==========//
	
	
	
	//===== Mise en place de la box de recherche =====//
	 var input = $('input#s');
    var divInput = $('div.input');
    var width = divInput.width();
    var outerWidth = divInput.parent().width() - (divInput.outerWidth() - width) - 28;
    var submit = $('#searchSubmit');
    var txt = input.val();
    
    input.bind('focus', function() {
        if(input.val() === txt) {
            input.val('');
        }
        $(this).animate({color: '#000'}, 300); // text color
        $(this).parent().animate({
            width: outerWidth + 'px',
            backgroundColor: '#fff', // background color
            paddingRight: '43px'
        }, 300, function() {
            if(!(input.val() === '' || input.val() === txt)) {
                if(!($.browser.msie && $.browser.version < 9)) {
                    submit.fadeIn(300);
                } else {
                    submit.css({display: 'block'});
                }
            }
        }).addClass('focus');
    }).bind('blur', function() {
        $(this).animate({color: '#b4bdc4'}, 300); // text color
        $(this).parent().animate({
            width: width + 'px',
            backgroundColor: '#e8edf1', // background color
            paddingRight: '15px'
        }, 300, function() {
            if(input.val() === '') {
                input.val(txt)
            }
        }).removeClass('focus');
        if(!($.browser.msie && $.browser.version < 9)) {
            submit.fadeOut(100);
        } else {
            submit.css({display: 'none'});
        }
    }).keyup(function() {
        if(input.val() === '') {
            if(!($.browser.msie && $.browser.version < 9)) {
                submit.fadeOut(300);
            } else {
                submit.css({display: 'none'});
            }
        } else {
            if(!($.browser.msie && $.browser.version < 9)) {
                submit.fadeIn(300);
            } else {
                submit.css({display: 'block'});
            }
        }
    });
    //=========//
	
	
	
	
	//===== Mise en place de l'animation de la page LOGIN =====//
	
	$('#bouton_connexion').click(
		function()
		{
			$('#bouton_connexion').css('background','rgba(200,14,31,1)');
			$('#bouton_creer_compte').css('background','rgba(200,14,31,.5)');
			$('#creer_compte').slideUp('fast',function()
			{
				$('#connexion').css('margin-left','-5px');
				$('#connexion').css('margin-right','-5px');
				$('#connexion').slideDown('slow');
			})
		});
		
	$('#bouton_creer_compte').click(
		function()
		{
			$('#bouton_connexion').css('background','rgba(200,14,31,.5)');
			$('#bouton_creer_compte').css('background','rgba(200,14,31,1)');
			$('#connexion').slideUp('fast',function()
			{
				$('#creer_compte').css('margin-left','-5px');
				$('#creer_compte').css('margin-right','-5px');
				$('#creer_compte').slideDown('slow');
			})
		});
		
	
	
	
	//===== Mise en place de l'animation de la page MON COMPTE =====//
	
	$('#bouton_favoris_user').click(
		function()
		{
			$('#bouton_favoris_user').css('background','rgba(200,14,31,1)');
			$('#bouton_thread_user').css('background','rgba(200,14,31,.5)');
			$('#bouton_settings').css('background','rgba(200,14,31,.5)');
			$('#gestion_thread, #settings').slideUp('fast',function()
			{
				$('#favoris_user').slideDown('slow');
			})
		})
	
	$('#bouton_thread_user').click(
		function()
		{
			$('#bouton_thread_user').css('background','rgba(200,14,31,1)');
			$('#bouton_favoris_user').css('background','rgba(200,14,31,.5)');
			$('#bouton_settings').css('background','rgba(200,14,31,.5)');
			$('#favoris_user, #settings').slideUp('fast',function()
			{
				$('#gestion_thread').slideDown('slow');
			})
		})
		
	$('#bouton_settings').click(
		function()
		{
			$('#bouton_settings').css('background','rgba(200,14,31,1)');
			$('#bouton_thread_user').css('background','rgba(200,14,31,.5)');
			$('#bouton_favoris_user').css('background','rgba(200,14,31,.5)');
			$('#favoris_user, #gestion_thread').slideUp('fast',function()
			{
				$('#settings').slideDown('slow');
			})
		})
})
	