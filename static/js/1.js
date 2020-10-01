function upload_image(){
  $("#input").unbind("change").bind("change",function(){ // bind: kiểm tra sự kiện là change
    let fileData=$(this).prop("files")[0];
    if(typeof (FileReader) != "undefined"){
        let imagePreview=$("#image-edit-profile");
        imagePreview.empty();// làm rỗng ;
        let fileReader=new FileReader();
        fileReader.onload=function(element){
          $("#cancel_crop_image").html(`<input style = "display:none" type="text" value="${element.target.result}" id="src_base64" name="image">`)
          let image_show = `<img src="${element.target.result}" id="image-show" class="" alt="Images" style="display: block; max-width: 350px; max-height : 50vh; margin:auto; padding : 2px; border : 1px solid white">`
          let image_main = `<img src="${element.target.result}" id="image-main" class="" alt="Images" style="display: none">`
          
          imagePreview.append(image_show)
          imagePreview.append(image_main)
        }
        imagePreview.show()
        fileReader.readAsDataURL(fileData);
    }
  })
}
function cancel_crop_image(){
   $("#cancel").unbind("click").bind("click", function(){
      let data_src = $("input#src_base64").val()
 	      let imagePreview=$("#image-edit-profile");
      imagePreview.empty();
      let image_show = `<img src="${data_src}" id="image-show" class="" alt="Images" style="display: block; width: 250px; height: 300px; margin:auto; border : 2px solid white">`
      imagePreview.append(image_show)
      imagePreview.show()
      $("#modal").modal('hide');
   })
}

function plate_detect(){
    $("button#send-image-plate").unbind('click').bind('click', function(){
        let data_src = $("input#src_base64").val()
        let brightness = $("input#brightness").val()
        let contrast = $("input#contrast").val()
        console.log(contrast, brightness, data_src)
        
    })
}

function received(){
  $("#received-image-plate").unbind("click").bind("click", function(){
      let data = $("img#image-show-plate").attr("src")
      // $("img#avatar").attr("src", data)

      let imagePreview=$("#image-edit-profile");
      imagePreview.empty();
      let image_show = `<img src="${data}" id="image-show" class="" alt="Images" style="display: block;max-width : 330px; max-height:300px; min-width:150px; min-height:40px; margin:auto; border : 2px solid white">`
      imagePreview.append(image_show)
      imagePreview.show()
      $("#cancel_crop_image").empty()
      $("#cancel_crop_image").append(`<input style = "display:none" type="text" value="${data}" id="src_base64" name= "image">`)
      $("#cancel_crop_image").show()
  })
}
$(document).ready(function(){
  upload_image()
  plate_detect()
  received()
  
})
