$(document).ready(function()
{
	
	
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
})
	