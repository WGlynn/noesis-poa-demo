//! Real Noesis core, in the browser. This wraps the ACTUAL `noesis-core`
//! `finalization::finalizes_pos_pom_fixed` — the same Q32.32 arithmetic the on-VM
//! finalization type-script calls — and exposes it to the demo's JS with a flat,
//! wasm-bindgen-free C ABI (numeric args only, no string marshaling).
#![no_std]

use core::alloc::{GlobalAlloc, Layout};
use noesis_core::finalization::{finalizes_pos_pom_fixed, ValidatorQ};

// noesis-core links `alloc`; finalizes_pos_pom_fixed itself never allocates, but the
// crate needs a global allocator to be defined in the final artifact. A tiny bump
// allocator (never frees) is sufficient and correct for our single-shot calls.
struct Bump;
static mut HEAP: [u8; 1 << 16] = [0; 1 << 16];
static mut OFF: usize = 0;
unsafe impl GlobalAlloc for Bump {
    unsafe fn alloc(&self, l: Layout) -> *mut u8 {
        let a = l.align();
        let off = (OFF + a - 1) & !(a - 1);
        let end = off + l.size();
        if end > HEAP.len() {
            return core::ptr::null_mut();
        }
        OFF = end;
        HEAP.as_mut_ptr().add(off)
    }
    unsafe fn dealloc(&self, _p: *mut u8, _l: Layout) {}
}
#[global_allocator]
static ALLOC: Bump = Bump;

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}

/// f64 -> Q32.32 (the core's fixed-point domain).
fn q(x: f64) -> u128 {
    (x * 4_294_967_296.0) as u128
}

fn mk(id: u64, stake: f64, standing: f64) -> ValidatorQ {
    ValidatorQ {
        id,
        pow: 0,
        pos: q(stake),
        pom: q(standing),
        last_heartbeat: 0,
    }
}

/// Fixed 4-actor finality check, computed by the REAL noesis-core rule.
/// `mask` bit i set => actor i is a signer. `threshold_bps` = 6667 for the 2/3 bar.
/// Returns 1 if the checkpoint finalizes, else 0. No decay (horizon=0, decay_pos=false).
#[no_mangle]
pub extern "C" fn floor_finalizes(
    s0: f64, d0: f64, s1: f64, d1: f64, s2: f64, d2: f64, s3: f64, d3: f64,
    mask: u32, threshold_bps: u32,
) -> i32 {
    let all = [mk(0, s0, d0), mk(1, s1, d1), mk(2, s2, d2), mk(3, s3, d3)];
    let mut voters = [mk(0, 0.0, 0.0), mk(0, 0.0, 0.0), mk(0, 0.0, 0.0), mk(0, 0.0, 0.0)];
    let mut n = 0usize;
    let mut i = 0usize;
    while i < 4 {
        if mask & (1u32 << i) != 0 {
            voters[n] = all[i].clone();
            n += 1;
        }
        i += 1;
    }
    finalizes_pos_pom_fixed(&voters[..n], &all, 0, 0, false, threshold_bps as u64) as i32
}
