//modal表示ボタンを全て取得
const editModalButtons = document.getElementsByName('editModalButton');

//読み込み時にドロップダウンボタンに関数を付与
document.addEventListener("DOMContentLoaded", function(){
    //すべてのtableを取得
    const tables = document.getElementsByName('table');
    //tableの中のtd要素数が6個ない場合は空白のtd要素を動的に作成
    for(let i=0; i<tables.length; i++){
        //tdの要素数を取得
        const trContentCounter = tables[i].cells.length;
        //要素数が６個ない場合空白の要素を追加
        if (trContentCounter != 6){
            //空白の要素を４個作成する
            for(let n=1; n<5; n++){
                newCell = tables[i].insertCell(n)
                newCell.classList.add('border', 'px-4', 'py-2', 'text-center')
            }
        }else{;}
    };
    

    //dropdown buttonを格納
    const dropdownButton = document.getElementById('dropdownDefaultButton');
    dropdownButton.addEventListener("click", onClick, false);

    //editModalを取得
    const editModal = document.getElementById('authentication-editModal');
    //createModalを取得
    const createModal = document.getElementById('authentication-createModal');

    //editModal表示ボタンを全て取得
    const editModalButtons = document.getElementsByName('editModalButton');

    //editModal表示ボタンに関数を付与
    for(let i=0; i<editModalButtons.length; i++){
        editModalButtons[i].addEventListener("click", {target: editModal, handleEvent: openEditModal, arg: i}, false);
    };

    //createModal表示ボタンに関数を付与
    const createModalButton = document.getElementById('createModalButton');
    if (createModalButton){
        createModalButton.addEventListener('click', {target: createModal, handleEvent: openCreateModal}, false);
    } else{;}

    //editmodal閉じるボタンを取得
    const closeEditButton = document.getElementById('closeEditModalButton');
    closeEditButton.addEventListener('click', {target: editModal, handleEvent: closeModal}, false);

    //createmodal閉じるボタンを取得
    const closeCreateButton = document.getElementById('closeCreateModalButton');
    closeCreateButton.addEventListener('click', {target: createModal, handleEvent: closeModal}, false);

},
false);


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

//editModalを表示する関数
function openEditModal(e){
    //editModalの要素を取得
    const editModalDate = document.getElementById('edit-modal-date');
    const editModalAttendance = document.getElementById('edit-modal-attendance');
    const editModalClosing = document.getElementById('edit-modal-closing');
    const editModalBreak = document.getElementById('edit-modal-break');
    const editModalContent = document.getElementById('edit-modal-content');
    const targetObj = document.getElementsByName('target-obj')[0];

    //editModalの中の値を動的に描画
    editModalDate.textContent = editModalButtons[this.arg].dataset.date + editModalButtons[this.arg].dataset.weekday
    if (editModalButtons[this.arg].dataset.attendance) {
        //出勤時間、退勤時間、休憩時間はそれぞれtimefieldのためvalueに値を入れた
        editModalAttendance.value = editModalButtons[this.arg].dataset.attendance
    }else{
        ;
    }
    if (editModalButtons[this.arg].dataset.closing) {
        editModalClosing.value = editModalButtons[this.arg].dataset.closing
    }else{
        ;
    }
    if (editModalButtons[this.arg].dataset.break) {
        editModalBreak.value = editModalButtons[this.arg].dataset.break
    }else{
        ;
    }if (editModalButtons[this.arg].dataset.break) {
        editModalContent.value = editModalButtons[this.arg].dataset.content
    }else{
        ;
    }

    targetObj.value = editModalButtons[this.arg].dataset.date


    //modalのclassからhiddenを外す
    this.target.classList.remove('hidden');

    //スクロールできないようbodyにoverflow-hiddenをつける
    document.body.classList.add('overflow-hidden');
};

//createModalを表示する関数
function openCreateModal(e){

    //createModalのclassからhiddenを外す
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