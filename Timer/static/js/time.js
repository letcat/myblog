
   var time;
   var status=0;
   var thentime;
   var result=new Array();
   var num=0;
  
   function showtime(){   
       var nowtime=new Date();
       time=nowtime.getTime()-thentime.getTime();
   
       if (time<1000){                  //小于一秒
	       minute_is="";
	       second_is="0.";
	       ss=Math.floor(time/10);
	       if (ss<10){ 	
		       ss_is="0"+ss;
			   }
		   else {
		       ss_is=ss;
			   }
        }
       else if (time<60000){			 //小于一分钟
           minute_is="";
           second=Math.floor(time/1000);
           if(second<10){
		       second_is="0"+second+".";
			}
		   else{
		       second_is=second+".";
			   }
	 	   ss=Math.floor((time%1000)/10);
	       if (ss<10){	
		       ss_is="0"+ss;
			   }
		  else {
		       ss_is=ss;
			   }
        }
       else {                           //大于一分钟
	      totalsecond=Math.floor(time/1000);//how many seconds?
	      second=totalsecond%60; //how many seconds-60*n
	      if(second<10){
		      second_is="0"+second+".";
		    }
		  else{
		      second_is=second+".";
			  }
		
	   minute=(totalsecond-second)/60; //how many minutes?
	   if(  minute<10){
			minute_is="0"+ minute+":";
	   }else{	
			minute_is=minute+":";
		}	
	   ss=Math.floor((time%1000)/10);
	   if (ss<10){	
		    ss_is="0"+ss;
       }else{
		    ss_is=ss;
		}	
	}
    finaltime=minute_is+second_is+ss_is;
    document.getElementById("num").innerHTML=finaltime;
    timeset= setTimeout("showtime()",20);
   }
   
 //开始
function start(event){
 
   if(event.keyCode==32){
	   event.preventDefault();
           if(status==0){
               thentime=new Date();
               $('#num').removeAttr('color');
               $('#num').css('color','red');
               showtime();
               status=1;
           }else if(status==1){
               status=2;
            }else if(status==2){
               status=0;
               document.getElementById("num").innerHTML="0.00"; 
               upset();
               showresult();
               $('#num').removeAttr('color');
               $('#num').css('color','blue');
            }
    } 
}
   //停止
   function stop(event){
	   $('#num').removeAttr('color');
       $('#num').css('color','green');
       if(event.keyCode==32&&status==1){
    	 event.preventDefault();
         clearTimeout(timeset); 
         if(result.length==5)
    	     result.pop();
         result.push(finaltime);
         $('#num').removeAttr('color');
         $('#num').css('color','blue');
       }  
   }
   
  //打乱公式
  function upset(){
      var format=["R","L","U","D","F","B","'"];
      var upset=new Array();
      set=" ";
      //确保第一个数不是“'”  
      upset[0]=format[Math.floor(Math.random()*6)];  
   
      for(var j=1;j<25;j++){
          var k=Math.floor(Math.random()*7);
          upset[j]=format[k];
           
          if(upset[j]==upset[j-1] && upset[j]==upset[j-2] && j>2){    //处理xxx三个相同字母的情况 
		      var flag= upset[j];
	          while(flag==upset[j]){
		          upset[j]=format[Math.floor(Math.random()*7)];   
	            }
            }
        }
      for(var j=0;j<25;j++){
	      if(j>2 && upset[j-1]=="'" && upset[j]==upset[j-2]){//处理x'x的情况
		      var flag= upset[j];
		      while(flag==upset[j]){
			      upset[j]=format[Math.floor(Math.random()*6)];   
		        } 
	        }  
	      if(j>0 && upset[j]==upset[j-1]){
			upset[j]="2"; 
		  }
	      if(upset[j]=="'" && upset[j-1]==2){
			upset[j]="F"; 
		  }
	      set=set+upset[j]+" ";   
       }
     document.getElementById("upset").innerHTML=set;
   }
  
 //显示时间
   function showresult(){
       var j;
	   var all=0;
       for(j=0;j<5;j++){
	       if(result[j]!=undefined)
               $("tr:eq(1) td:eq("+j+")").html(result[j]);
	       else break;
        }
        if(j==5){
    	    for(var i=0;i<5;i++){
    	        all+=parseFloat(result[i]);
    	    }
            $("tr:eq(1) td:eq("+j+")").html((all/5).toFixed(3));  //toFixed(n)控制小数位数
            resultChart(result);  
       }    
 }
 function resultClear(event){
	  for(var j=0;j<5;j++){
			$("tr:eq(1) td:eq("+j+")").html("-");
	  }
	  result=[];
	  event.stopPropagation();
 }
//时间大于1minute 把时间转化为用秒表示
 function updateResultToSec(result){
	 var array =result;
	 for(var i =0;i<array.length;i++){
		 if(array[i].match(':')){	 
			var temp  = array[i].split(':');
			array [i] =parseFloat(temp[0]*60)+parseFloat(temp[1]);
		 }
	 }
     return array;
 }
 
 
//成绩图表
 function resultChart(result) {
	   var newresult = updateResultToSec(result);
              var max =Math.max.apply(null,newresult);
			  var min = Math.min.apply(null,newresult);
				var data = [
				         	{
				         		name : 'result',
				         		value:newresult,
				         		color:'#0d8ecf',
				         		line_width:1
				         	}
				         ];
		         
				var labels = ["01","02","03","04","05"];
				
				var line = new iChart.LineBasic2D({
					render : 'canvasDiv',
					data: data,
					fontsize:5,
					align:'center',
					title : 'Result',
					subtitle : '',
					footnote : '5 times',
					width : 700, //800
					height : 300, //400
					sub_option:{
						smooth : true,//平滑曲线
						point_size:10
					},
					tip:{
						enable:true,
						shadow:true
					},
					legend : {
						enable : false
					},
					crosshair:{
						enable:true,
						line_color:'#62bce9'
					},
					coordinate:{
						width:500,
						valid_width:300,
						height:260,
						axis:{
							color:'#9f9f9f',
							width:[0,0,2,2]
						},
						grids:{
							vertical:{
								way:'share_alike',
						 		value:5
							}
						},
						scale:[{
							 position:'left',	
							 start_scale:min-2*(max-min)/5,
							 end_scale:max+5*(max-min)/5, 
							 scale_space:((max-min)/5).toFixed(2),
							 scale_size:2,
							 scale_color:'#9f9f9f'
						},{
							 position:'bottom',	
							 scale_size:2,
							 labels:labels
						}]
					}
				});
			//开始画图
			line.draw();
  
               }
