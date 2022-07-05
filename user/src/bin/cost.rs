#![no_std]
#![no_main]

#[macro_use]
extern crate user_lib;
extern crate alloc;

use alloc::{vec::{ Vec}, sync::Arc, };
use lazy_static::lazy_static;
use spin::Mutex;
use user_lib::{thread_create, get_time, exit, shut_done, yield_};

struct Argument {
    _r: Arc<Mutex<Counter>>, 
    _w: Arc<Mutex<Counter>>, 
    _t: usize,
}

impl Argument {
    fn new(r: Arc<Mutex<Counter>>, w: Arc<Mutex<Counter>>, t: usize) -> Self {
        Self { _r: r, _w: w, _t: t }
    }
}

fn thread_main(arg: *const Argument) {
    let arg = unsafe { &*arg };
    let r = arg._r.clone();
    let w = arg._w.clone();
    let t = arg._t;

    //loop {
        read_cnt(r.clone(), t + 1);
        //println!("thread {}", t);
        write_cnt(w.clone(), t + 2);
    //}
    exit(0);
}

const THREAD_NUM: usize = 
4000
;

#[no_mangle]
pub fn main() -> i32 {
    let start = get_time() as usize;

    

    let first_write = Counter::new();
    let mut readi = first_write.clone();

    let mut args = Vec::new();

    for i in 0..THREAD_NUM {

        let next_rw = Counter::new();
        let next_w = next_rw.clone();

        args.push(Argument::new(readi.clone(), next_w.clone(), i));

        readi = next_rw.clone();
    }

    //println!("creat args done");

    let mut ts = Vec::new();

    for i in 0..THREAD_NUM {
        let arg = &args[i];
        ts.push(thread_create(thread_main as usize, arg as *const _ as usize));
    }

    //println!("creat threads done");

    // warm up
    //write_cnt(first_write.clone(), 1);
    //read_cnt(readi.clone(), THREAD_NUM + 1);

    //println!("warm up done");

    //let mut str = String::new();
    write_cnt(first_write.clone(), 1);
    read_cnt(readi.clone(), THREAD_NUM + 1);

    
    let end = get_time() as usize;
    println!(">>> {}", end - start);

    shut_done();
    0
}


lazy_static! {
    pub static ref COUNTER: Arc<Mutex<usize>> = Arc::new(Mutex::new(0));
}

pub struct Counter(usize);

impl Counter {
    pub fn new() -> Arc<Mutex<Self>> {
        Arc::new(Mutex::new(Self(0)))
    }
}

#[allow(unused_must_use)]
pub fn write_cnt(cnter: Arc<Mutex<Counter>>, target: usize) {
    cnter.lock().0 = target;
}


pub fn read_cnt(cnter: Arc<Mutex<Counter>>, target: usize) {
    while cnter.lock().0 != target { yield_(); }
    cnter.lock().0 = 0;
    //println!("read {} ok", target);
}