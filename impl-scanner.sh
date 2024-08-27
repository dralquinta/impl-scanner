
__install_prereqs(){
    echo '============== Virtual Environment Creation =============='
    python3 -m venv venv
    source venv/bin/activate

    echo '============== Upgrading pip3 =============='
    pip3 install --upgrade pip

    echo '============== Installing requirements =============='
    pip3 install -r requirements.txt
}




__call_impl-scanner(){
    python3 impl-scanner.py 
}


__start_impl-scanner(){

    __call_impl-scanner

}



__main__(){ 
if [ ! -d ".venv" ]; then
  __install_prereqs
fi
    __start_impl-scanner
}


__main__