import { useRef, useMemo } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';

function Particles({ count = 120 }) {
  const ref = useRef<THREE.Points>(null);

  const [positions, colors, sizes] = useMemo(() => {
    const pos = new Float32Array(count * 3);
    const col = new Float32Array(count * 3);
    const siz = new Float32Array(count);

    const colorA = new THREE.Color('#6366f1');
    const colorB = new THREE.Color('#8b5cf6');
    const colorC = new THREE.Color('#14b8a6');

    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 18;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 18;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 12;

      const t = Math.random();
      const color = t < 0.4 ? colorA : t < 0.7 ? colorB : colorC;
      col[i * 3] = color.r;
      col[i * 3 + 1] = color.g;
      col[i * 3 + 2] = color.b;

      siz[i] = Math.random() * 0.04 + 0.01;
    }
    return [pos, col, siz];
  }, [count]);

  useFrame((state) => {
    if (ref.current) {
      ref.current.rotation.y = state.clock.elapsedTime * 0.015;
      ref.current.rotation.x = state.clock.elapsedTime * 0.008;
    }
  });

  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" count={count} array={positions} itemSize={3} />
        <bufferAttribute attach="attributes-color" count={count} array={colors} itemSize={3} />
      </bufferGeometry>
      <pointsMaterial
        size={0.04}
        vertexColors
        transparent
        opacity={0.6}
        sizeAttenuation
        blending={THREE.AdditiveBlending}
        depthWrite={false}
      />
    </points>
  );
}

function FloatingRing({ radius = 3, tubeRadius = 0.005, position = [0, 0, -5] as [number, number, number], speed = 0.03 }) {
  const ref = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (ref.current) {
      ref.current.rotation.x = state.clock.elapsedTime * speed;
      ref.current.rotation.z = state.clock.elapsedTime * speed * 0.7;
      ref.current.position.y = Math.sin(state.clock.elapsedTime * 0.2) * 0.3;
    }
  });

  return (
    <mesh ref={ref} position={position} scale={1}>
      <torusGeometry args={[radius, tubeRadius, 64, 128]} />
      <meshBasicMaterial color="#6366f1" transparent opacity={0.08} />
    </mesh>
  );
}

function GradientSphere() {
  const ref = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (ref.current) {
      ref.current.rotation.y = state.clock.elapsedTime * 0.04;
      ref.current.rotation.x = state.clock.elapsedTime * 0.02;
      ref.current.position.y = Math.sin(state.clock.elapsedTime * 0.3) * 0.2;
    }
  });

  return (
    <mesh ref={ref} position={[0, 0, -5]} scale={3.5}>
      <icosahedronGeometry args={[1, 1]} />
      <meshBasicMaterial
        color="#8b5cf6"
        transparent
        opacity={0.03}
        wireframe
      />
    </mesh>
  );
}

function MouseLight() {
  const light = useRef<THREE.PointLight>(null);
  const { viewport } = useThree();

  useFrame((state) => {
    if (light.current) {
      light.current.position.x = (state.pointer.x * viewport.width) / 2;
      light.current.position.y = (state.pointer.y * viewport.height) / 2;
    }
  });

  return <pointLight ref={light} intensity={0.5} color="#6366f1" distance={8} />;
}

export default function HeroCanvas() {
  return (
    <div style={{
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
    }}>
      <Canvas
        camera={{ position: [0, 0, 5], fov: 60 }}
        style={{ background: 'transparent' }}
        dpr={[1, 1.5]}
      >
        <ambientLight intensity={0.1} />
        <MouseLight />
        <Particles count={120} />
        <GradientSphere />
        <FloatingRing radius={2.5} position={[0, 0, -4]} speed={0.025} />
        <FloatingRing radius={4} tubeRadius={0.003} position={[1, -0.5, -7]} speed={0.015} />
      </Canvas>
    </div>
  );
}
