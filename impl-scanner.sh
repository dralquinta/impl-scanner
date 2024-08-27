
__install_prereqs(){
    echo '============== Virtual Environment Creation =============='
    python3 -m venv venv
    source venv/bin/activate
    

    echo '============== Upgrading pip3 =============='
    pip3 install --upgrade pip

    echo '============== Installing requirements =============='
    pip3 install -r requirements.txt
}


__create_venv(){
    if [ ! -d "venv" ] 
    then
        echo "venv not present. Creating" 
        __install_prereqs
        chmod -R 775 venv
    fi

    source "./venv/bin/activate"

}




__call_impl_scanner(){
    python3 impl-scanner.py 
}






__main__(){ 
    __create_venv
    __call_impl_scanner
}


__main__