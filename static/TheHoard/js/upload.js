console.log("KWAME is a boy")


const uploadForm = document.getElementById("upload-form")
const input = document.getElementById("id_file")
console.log(input)
console.log(uploadForm)

const alertBox = document.getElementById('alert-box')
const videoBox = document.getElementById('video-box')
const progressBox = document.getElementById('progress-box')
const cancelBox = document.getElementById('cancel-box')
const cancelBtn = document.getElementById('cancel-btn')

comment_btn = document.getElementById('comment-btn')
reply_btn = document.getElementById('reply-btn')
comment_input = document.getElementById('comment-input')
reply_input = document.getElementById('reply-input')
console.log(comment_input[0].value)

const csrf = document.getElementsByName('csrfmiddlewaretoken')
console.log(csrf)
input.addEventListener('change', ()=>{
    progressBox.classList.remove('invisible')
    cancelBox.classList.remove('invisible')

    const vid_data = input.files[0]
    console.log(vid_data)

    const fd = new FormData
    fd.append('csrfmiddlewaretoken',csrf[0].value )
    fd.append('path',vid_data)

    $.ajax({
        type:'POST',
        url: uploadForm.action,
        enctype: 'multipart/form-data',
        data: fd,
        beforeSend: function(){

        },
        xhr: function(){
            const xhr = new window.XMLHttpRequest()
            xhr.upload.addEventListener('progress',e =>{
                console.log(e)
            })

            return xhr

        },
        success: function(response){

        },
        error: function(response){

        },
        cache: false,
        contentType: false,
        processData: false

    })
})


