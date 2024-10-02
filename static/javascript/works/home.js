//メニューを表示させる関数
function onClick(){
    const target = document.getElementById('dropdown');
    //メニューのclassにhiddenがあるか確認
    result = target.classList.contains('hidden');
    
    //hiddenがある場合それを除く,ない場合は追加する
    if (result){
        target.classList.remove('hidden');
    } else{
        target.classList.add('hidden');
    }

};

//modalを表示する関数
function openModal(e){
    //modalのclassからhiddenを外す
    this.target.classList.remove('hidden');

    //スクロールできないようbodyにoverflow-hiddenをつける
    document.body.classList.add('overflow-hidden');
};

//modalを閉じる関数
function closeModal(e){
    this.target.classList.add('hidden');

    //bodyからoverflow-hiddenを外す
    document.body.classList.remove('overflow-hidden');
};

//読み込み時にドロップダウンボタンに関数を付与
document.addEventListener("DOMContentLoaded", function(){

    //dropdown buttonを格納
    const dropdownButton = document.getElementById('dropdownDefaultButton');
    dropdownButton.addEventListener("click", onClick, false);

    //modalを取得
    const modal = document.getElementById('authentication-modal');

    //modal表示ボタンを全て取得
    const modalButtons = document.getElementsByName('modalButton');
    //modal表示ボタンに関数を付与
    for(let i=0; i<modalButtons.length; i++){
        modalButtons[i].addEventListener("click", {target: modal, handleEvent: openModal}, false);
    };

    //modal閉じるボタンを取得
    const closeButton = document.getElementById('closeButton');
    closeButton.addEventListener('click', {target: modal, handleEvent: closeModal}, false);

},
false);