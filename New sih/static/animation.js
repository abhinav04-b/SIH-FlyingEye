document.addEventListener("DOMContentLoaded", (event)=> {
    gsap.registerPlugin(ScrollTrigger)
    gsap.matchMedia()
    .add("(min-width: 786px)", () => {
        const tl = gsap.timeline({
            scrollTrigger: {
                trigger: "#home",
                markers: false,
                scrub: 2,
                pin: true,
                start: "50% 50%",
                end: "150% 50%"
            },
        });
        tl.to("#flying_eye",{
            opacity:"-1",
        },'a')
        tl.to("#logo",{
            opacity:"5"
        },'a')
        tl.to("#m_abt",{
            scale:"1.1"
        },'b')
        tl.to("#m_abt",{
            scale:"0"
        },'c')
        tl.to("#s11",{
            top:"0"
        },'d')
        tl.to("#s12",{
            top:"0"
        },'e')
        tl.to("#s13",{
            top:"0"
        },'f')
        tl.to(".comtainer_img img",{
            top:'-100%'
        },'g')
        tl.to("#about1",{
            display:"block"
        },'h')
        tl.to("#about2",{
            display:"block"
        },'h')
        tl.to("#ai_btn",{
            display:"block"
        },'i')
        tl.to("#f1_btn",{
            display:"block"
        },'j')
        tl.to("#s_btn",{
            display:"block"
        },'k')
    })
})