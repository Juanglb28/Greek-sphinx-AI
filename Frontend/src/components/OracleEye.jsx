import { motion } from 'framer-motion';

export default function OracleEye({ state }) {
    // state: 'idle', 'loading', 'active', 'success', 'failure'

    const variants = {
        idle: { scale: 1, opacity: 0.5, filter: 'hue-rotate(0deg)' },
        loading: { scale: [1, 1.2, 1], opacity: 0.8, transition: { repeat: Infinity, duration: 2 } },
        active: { scale: 1.1, opacity: 1, filter: 'drop-shadow(0 0 20px var(--color-oracle))' },
        success: { scale: 1.2, filter: 'hue-rotate(90deg) drop-shadow(0 0 30px gold)' },
        failure: { scale: 0.9, filter: 'hue-rotate(-90deg) drop-shadow(0 0 30px red)' },
    };

    return (
        <div className="oracle-eye-container flex-center" style={{ height: '300px', position: 'relative' }}>
            <motion.div
                className="oracle-eye-outer"
                animate={state}
                variants={variants}
                style={{
                    width: '200px',
                    height: '200px',
                    borderRadius: '50%',
                    border: '2px solid var(--color-gold)',
                    position: 'absolute',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    background: 'radial-gradient(circle, var(--color-mystic) 0%, var(--color-void) 100%)',
                    boxShadow: 'var(--glow-gold)'
                }}
            >
                <motion.div
                    className="oracle-eye-inner"
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 10, ease: "linear" }}
                    style={{
                        width: '140px',
                        height: '140px',
                        border: '1px dashed var(--color-oracle)',
                        borderRadius: '50%'
                    }}
                />
                <div style={{ position: 'absolute', fontSize: '4rem' }}>
                    👁️
                </div>
            </motion.div>
        </div>
    );
}
