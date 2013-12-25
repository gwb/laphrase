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
	