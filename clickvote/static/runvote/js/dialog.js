
var XMLHttpRequestObject = false;

if (window.XMLHttpRequest) {
	XMLHttpRequestObject = new XMLHttpRequest();
	XMLHttpRequestObject.overrideMimeType("text/xml"); // Set the format the datatype you are working with for none microsoft browsers
	
} else if (window.ActiveXObject) {
	XMLHttpRequestObject = new ActiveXObject("Microsoft.XMLHTTP");
}





function customAlert() {
	this.render = function(dialog){
		var winW = window.innerWidth;
		var winH = window.innerHeight;
		var dialogoverlay = document.getElementById('dialogoverlay');
		var dialogbox = document.getElementById('dialogbox');
		dialogoverlay.style.display = "block";
		dialogoverlay.style.height = winH+"px";
		dialogbox.style.left = (winW/2) - (550 * .5)+"px";
		dialogbox.style.top = "100px";
		dialogbox.style.display = "block";
		document.getElementById('dialogboxhead').innerHTML = "Aknowledge This message";
		document.getElementById('dialogboxbody').innerHTML = dialog;
		document.getElementById('dialogboxfoot').innerHTML = '<button onclick= "Alert.ok()">OK</button>';
	}

	this.ok = function(){
		document.getElementById('dialogbox').style.display = "none";
		 document.getElementById('dialogoverlay').style.display = "none";

	}

	this.no = function(){

	}

	this.yes = function(){

	}
}

var Alert = new customAlert();



function customConfirm(){
	this.render = function(dialog, sid, crid, ceid, eid){
		var winW = window.innerWidth;
		var winH = window.innerHeight;
		var dialogoverlay = document.getElementById('dialogoverlay');
		var dialogbox = document.getElementById('dialogbox');
		dialogoverlay.style.display = "block";
		dialogoverlay.style.height = winH+"px";
		//dialogbox.style.left = (winW/2) - (550 * .5)+"px";
		dialogbox.style.top = "100px";
		dialogbox.style.display = "block";
                if(dialog !== 'skip')
		var cname = document.getElementById('sp_'+crid).innerHTML;

		if(dialog === 'YES'){
		document.getElementById('dialogboxhead').innerHTML = "Confirm Vote";
		document.getElementById('dialogboxbody').innerHTML = 'Are you sure you want to vote ' + dialog + ' for' + ' '+ cname + '?';
		document.getElementById('dialogboxfoot').innerHTML = '<button class = "btnbtn"onclick="confirm.yes(\''+sid+'\',\''+crid
			+'\')">Yes</button> <button class = "btnbtn" onclick="confirm.no()">No</button>';

		this.yes = function(){
				voteCandidate(sid, crid, ceid, eid);

			document.getElementById('dialogbox').style.display = "none";
			document.getElementById('dialogoverlay').style.display = "none";
		}

		this.no = function(){
			document.getElementById('dialogbox').style.display = "none";
			document.getElementById('dialogoverlay').style.display = "none";
		}
	}else if(dialog === 'NO'){

				document.getElementById('dialogboxhead').innerHTML = "Confirm Vote";
		document.getElementById('dialogboxbody').innerHTML = 'Are you sure you want to vote ' + dialog + ' for' + ' '+ cname + '?';
		document.getElementById('dialogboxfoot').innerHTML = '<button class = "btnbtn"onclick="confirm.yes(\''+sid+'\',\''+crid
			+'\')">Yes</button> <button class = "btnbtn" onclick="confirm.no()">No</button>';

		this.yes = function(){
				var str = 'no';
				voteCandidate(sid, str, ceid, eid);

			document.getElementById('dialogbox').style.display = "none";
			document.getElementById('dialogoverlay').style.display = "none";
		}

		this.no = function(){
			document.getElementById('dialogbox').style.display = "none";
			document.getElementById('dialogoverlay').style.display = "none";
		}

	}else if(dialog === 'vote'){

		document.getElementById('dialogboxhead').innerHTML = "Confirm Vote";
		document.getElementById('dialogboxbody').innerHTML = 'Are you sure you want to ' + dialog + ' for' + ' '+ cname + '?';
		document.getElementById('dialogboxfoot').innerHTML = '<button class = "btnbtn"onclick="confirm.yes(\''+sid+'\',\''+crid
			+'\')">Yes</button> <button class = "btnbtn" onclick="confirm.no()">No</button>';

		this.yes = function(){
				voteCandidate(sid, crid, ceid, eid);

			document.getElementById('dialogbox').style.display = "none";
			document.getElementById('dialogoverlay').style.display = "none";
		}

		this.no = function(){
			document.getElementById('dialogbox').style.display = "none";
			document.getElementById('dialogoverlay').style.display = "none";
		}


	}else if(dialog === 'skip'){

				document.getElementById('dialogboxhead').innerHTML = "Confirm Skip";
		document.getElementById('dialogboxbody').innerHTML = 'Are you sure you want to ' + dialog + '?';
		document.getElementById('dialogboxfoot').innerHTML = '<button class = "btnbtn"onclick="confirm.yes(\''+sid+'\',\''+crid
			+'\')">Yes</button> <button class = "btnbtn" onclick="confirm.no()">No</button>';

		this.yes = function(){
				var str = 'skip';
				voteCandidate(sid, str, ceid, eid);

			document.getElementById('dialogbox').style.display = "none";
			document.getElementById('dialogoverlay').style.display = "none";
		}
                this.no = function(){
			document.getElementById('dialogbox').style.display = "none";
			document.getElementById('dialogoverlay').style.display = "none";
		}
		
	}
}
}

var confirm = new customConfirm();

