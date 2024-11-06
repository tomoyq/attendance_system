//タブボタンとタブコンテンツを取得
const tabButtons = document.getElementsByClassName('tab-button')
const tabContents = document.getElementsByClassName('content')

//背景色を変えるためのdiv要素
const loginContent = document.getElementById('loginContent')

function onClick(){

    //全てのタブボタンとタブコンテンツからis-activeを外す
    for(let j = 0; j < tabButtons.length; j++){
        tabButtons[j].classList.remove('is-active');
        tabContents[j].classList.remove('is-active');
    };

    //押されたタブボタンにis-activeを追加
    this.classList.add('is-active');

    //タブボタンに紐づくコンテンツにis-activeを追加
    const targetContent =document.getElementById(this.id + '-content');
    targetContent.classList.add('is-active');

    //背景にbg-primaryがあるか確認
    result = loginContent.classList.contains('bg-primary-100');
    //ない場合は追加
    if(result){
        loginContent.classList.remove('bg-primary-100');
    } else {
        loginContent.classList.add('bg-primary-100');
    };
};

document.addEventListener("DOMContentLoaded", function(){
    
    //タブボタンごとにクリックイベントを追加
    for(let i=0; i<tabButtons.length; i++){
        tabButtons[i].addEventListener("click", onClick, false);
    };

    //管理者ログインの入力エラーで再描画されたか判定
    if (document.getElementById("admin-login-form-error") != null){
        //管理者ログインの入力エラーだった場合'管理者ログイン'タブをクリックする
        tabButtons[1].click();
    }else{;};
},
false);

