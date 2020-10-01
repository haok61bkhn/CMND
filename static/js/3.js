var avatar = document.getElementById('avatar');
var image = document.getElementById('image');
var input = document.getElementById('input');
var $modal = $('#modal');
var cropper;

function change_input(){
  $("#input").unbind("change").bind('change', function (e) {
    let fileData=$(this).prop("files")[0];
    console.log(fileData)
    var files = e.target.files;
    var done = function (url) {
      input.value = '';
      image.src = url;
      $modal.modal('show');
    };
    var reader;
    var file;
    var url;

    if (files && files.length > 0) {
      file = files[0];

      if (URL) {
        done(URL.createObjectURL(file));
      } else if (FileReader) {
        reader = new FileReader();
        reader.onload = function (e) {
          console.log(e.target.result)
          console.log(render.result)
          done(reader.result);
        };
        reader.readAsDataURL(file);
      }
      $("#cancel_crop_image").empty()
      let fileReader=new FileReader();
      fileReader.onload=function(element){
          // console.log(element.target.result)
          // $("input#src_base64").val(element.target.result)
          $("#cancel_crop_image").append(`<input style = "display:none" type="text" value="${element.target.result}" id="src_base64" name="image">`)
      }
      $("#cancel_crop_image").show()
      fileReader.readAsDataURL(fileData);
    }
  });
}
function model_show(){
  $modal.on('shown.bs.modal', function () {
    cropper = new Cropper(image, {
      viewMode: 3,
    });
  }).on('hidden.bs.modal', function () {
    cropper.destroy();
    cropper = null;
  });
}

function crop_image(){
    $("#crop").bind('click', function () {
      let imagePreview=$("#image-edit-profile");
      imagePreview.empty();
      var initialAvatarURL;
      var canvas;
      $modal.modal('hide');
      $("input#brightness").val(100)
      $("input#contrast").val(100)
      if (cropper) {
          canvas = cropper.getCroppedCanvas({
            width: 350,
            height: 250,
          });
          initialAvatarURL = avatar.src;
          avatar.src = canvas.toDataURL();
          $("#cancel_crop_image").empty()
          $("#cancel_crop_image").append(`<input style = "display:none" type="text" value="${avatar.src}" id="src_base64" name="image">`)
          $("#cancel_crop_image").show()
          let image_show = `<img src="${avatar.src}" id="image-show" class="" alt="Images" style="display: block; width: ${canvas.width + 50}; height: ${canvas.height +  30}; margin:auto; border : 2px solid white">`
          imagePreview.append(image_show)
          imagePreview.show()
        }
    });
}
$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
  change_input()
  model_show()
  crop_image()
})
