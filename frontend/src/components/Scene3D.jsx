import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Float } from '@react-three/drei';

function FloatingGeometry() {
  const group = useRef();
  
  useFrame((state, delta) => {
    group.current.rotation.y += delta * 0.1;
    group.current.rotation.x += delta * 0.05;
  });

  return (
    <group ref={group}>
      {[...Array(25)].map((_, i) => (
        <Float key={i} speed={1.5 + Math.random()} rotationIntensity={1.5} floatIntensity={2.5}>
          <mesh position={[(Math.random() - 0.5) * 20, (Math.random() - 0.5) * 20, (Math.random() - 0.5) * 10 - 5]}>
            {i % 3 === 0 ? <boxGeometry args={[1, 1, 1]} /> : i % 3 === 1 ? <octahedronGeometry args={[1]} /> : <torusGeometry args={[0.7, 0.2, 16, 100]} />}
            <meshStandardMaterial 
              color={i % 2 === 0 ? "#3b82f6" : "#8b5cf6"} 
              opacity={0.4} 
              transparent 
              wireframe={i % 4 === 0} 
            />
          </mesh>
        </Float>
      ))}
    </group>
  );
}

export default function Scene3D() {
  return (
    <div className="fixed inset-0 z-0 pointer-events-none opacity-60">
      <Canvas camera={{ position: [0, 0, 10], fov: 60 }}>
        <ambientLight intensity={0.4} />
        <pointLight position={[10, 10, 10]} intensity={1} color="#60a5fa" />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#c084fc" />
        <Stars radius={100} depth={50} count={3000} factor={4} saturation={0} fade speed={1} />
        <FloatingGeometry />
        <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.5} />
      </Canvas>
    </div>
  );
}
