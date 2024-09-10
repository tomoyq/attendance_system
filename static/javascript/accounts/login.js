//タブボタンとタブコンテンツを取得
const tabButtons = document.getElementsByClassName('tab-button')
const tabContents = document.getElementsByClassName('content')

function onClick(){
    //全てのタブボタンとタブコンテンツからis-activeを外す
    for(let j = 0; j < tabButtons.length; j++){
        tabButtons[j].classList.remove('is-active');
        tabContents[j].classList.remove('is-active');
    };

    //押されたタブボタンにis-activeを追加
    this.classList.add('is-active');

    //タブボタンに紐づくコンテンツにis-activeを追加
    const targetContent =document.getElementById('content' + this.id);
    targetContent.classList.add('is-active');
};

document.addEventListener("DOMContentLoaded", function(){

    //タブボタンごとにクリックイベントを追加
    for(let i=0; i<tabButtons.length; i++){
        tabButtons[i].addEventListener("click", onClick, false);
    };

},
false);

