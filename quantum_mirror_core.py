"""
Quantum Mirror Theory - Core Mathematical Implementation
Mathematical framework for the Mirror Equation: |Ψ⟩ ≡ M|Ψ'⟩
"""

import numpy as np
from scipy.linalg import expm, sqrtm
from typing import Tuple, Optional, Union
import warnings

# Suppress potential numerical warnings for cleaner output
warnings.filterwarnings('ignore', category=RuntimeWarning)


class QuantumState:
    """
    Represents a quantum state in arbitrary dimension (qudit).
    Supports both pure states and density matrices.
    """
    
    def __init__(self, state: np.ndarray, is_density_matrix: bool = False):
        """
        Initialize quantum state.
        
        Args:
            state: State vector (1D array) or density matrix (2D array)
            is_density_matrix: If True, treat as density matrix
        """
        self.state = np.array(state, dtype=complex)
        self.is_density_matrix = is_density_matrix
        
        if not is_density_matrix:
            # Normalize state vector
            norm = np.linalg.norm(self.state)
            if norm > 0:
                self.state = self.state / norm
            self.dimension = len(self.state)
        else:
            # Verify density matrix properties
            self.dimension = self.state.shape[0]
            self._normalize_density_matrix()
    
    def _normalize_density_matrix(self):
        """Normalize density matrix to ensure Tr(ρ) = 1"""
        trace = np.trace(self.state)
        if abs(trace) > 1e-10:
            self.state = self.state / trace
    
    def to_density_matrix(self) -> np.ndarray:
        """Convert state to density matrix representation"""
        if self.is_density_matrix:
            return self.state
        else:
            return np.outer(self.state, np.conj(self.state))
    
    def get_state_vector(self) -> Optional[np.ndarray]:
        """Get state vector if pure state, None otherwise"""
        if not self.is_density_matrix:
            return self.state
        
        # Check if density matrix represents a pure state
        eigenvalues = np.linalg.eigvalsh(self.state)
        if np.sum(eigenvalues > 1e-10) == 1:
            # Pure state - extract state vector
            eigvals, eigvecs = np.linalg.eigh(self.state)
            idx = np.argmax(eigenvalues)
            return eigvecs[:, idx]
        return None
    
    def purity(self) -> float:
        """Calculate purity: Tr(ρ²)"""
        rho = self.to_density_matrix()
        return np.real(np.trace(rho @ rho))
    
    def von_neumann_entropy(self) -> float:
        """Calculate von Neumann entropy: -Tr(ρ log ρ)"""
        rho = self.to_density_matrix()
        eigenvalues = np.linalg.eigvalsh(rho)
        eigenvalues = eigenvalues[eigenvalues > 1e-15]  # Remove numerical zeros
        return -np.sum(eigenvalues * np.log(eigenvalues))


class MirrorOperator:
    """
    Implements the Mirror Operator M with properties:
    - M² = I (involution)
    - M† = M (Hermitian)
    - [M, H] = 0 (conserved with Hamiltonian)
    """
    
    def __init__(self, dimension: int, operator_type: str = 'reflection'):
        """
        Initialize Mirror Operator.
        
        Args:
            dimension: Hilbert space dimension (d for qudit)
            operator_type: Type of mirror operator
                - 'reflection': Simple reflection operator
                - 'parity': Parity operator
                - 'custom': Custom Hermitian involution
        """
        self.dimension = dimension
        self.operator_type = operator_type
        self.M = self._construct_operator()
        self._verify_properties()
    
    def _construct_operator(self) -> np.ndarray:
        """Construct the mirror operator based on type"""
        d = self.dimension
        
        if self.operator_type == 'reflection':
            # Simple reflection: |i⟩ → |d-1-i⟩
            M = np.zeros((d, d), dtype=complex)
            for i in range(d):
                M[i, d-1-i] = 1.0
            return M
        
        elif self.operator_type == 'parity':
            # Parity operator: (-1)^n for position states
            M = np.diag([(-1)**i for i in range(d)])
            return M.astype(complex)
        
        elif self.operator_type == 'custom':
            # Random Hermitian involution
            # Generate random Hermitian matrix with eigenvalues ±1
            eigenvalues = np.random.choice([-1, 1], size=d)
            # Random unitary matrix
            A = np.random.randn(d, d) + 1j * np.random.randn(d, d)
            Q, _ = np.linalg.qr(A)
            M = Q @ np.diag(eigenvalues) @ Q.conj().T
            return M
        
        else:
            raise ValueError(f"Unknown operator type: {self.operator_type}")
    
    def _verify_properties(self) -> bool:
        """Verify M² = I and M† = M"""
        # Check involution: M² = I
        M_squared = self.M @ self.M
        identity = np.eye(self.dimension)
        involution_error = np.linalg.norm(M_squared - identity)
        
        # Check Hermitian: M† = M
        hermitian_error = np.linalg.norm(self.M - self.M.conj().T)
        
        tolerance = 1e-10
        if involution_error > tolerance or hermitian_error > tolerance:
            print(f"Warning: Operator properties not satisfied:")
            print(f"  Involution error: {involution_error}")
            print(f"  Hermitian error: {hermitian_error}")
            return False
        return True
    
    def apply(self, state: QuantumState) -> QuantumState:
        """Apply mirror operator to quantum state"""
        if state.is_density_matrix:
            # ρ' = M ρ M†
            new_state = self.M @ state.state @ self.M.conj().T
            return QuantumState(new_state, is_density_matrix=True)
        else:
            # |Ψ'⟩ = M|Ψ⟩
            new_state = self.M @ state.state
            return QuantumState(new_state, is_density_matrix=False)
    
    def commutator_with(self, H: np.ndarray) -> np.ndarray:
        """Calculate commutator [M, H]"""
        return self.M @ H - H @ self.M
    
    def eigendecomposition(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get eigenvalues and eigenvectors of M"""
        eigenvalues, eigenvectors = np.linalg.eigh(self.M)
        return eigenvalues, eigenvectors


class MirrorConstant:
    """
    Calculate and analyze the Mirror Constant 𝕄 = ⟨Ψ|M|Ψ'⟩
    For perfectly coherent systems, 𝕄 = 1
    """
    
    @staticmethod
    def calculate(observer_state: QuantumState, 
                  reflection_state: QuantumState,
                  mirror_op: MirrorOperator) -> complex:
        """
        Calculate Mirror Constant: 𝕄 = ⟨Ψ|M|Ψ'⟩
        
        Args:
            observer_state: Observer state |Ψ⟩
            reflection_state: Reflection state |Ψ'⟩
            mirror_op: Mirror operator M
            
        Returns:
            Complex number representing mirror constant
        """
        psi = observer_state.get_state_vector()
        psi_prime = reflection_state.get_state_vector()
        
        if psi is None or psi_prime is None:
            raise ValueError("States must be pure for mirror constant calculation")
        
        # 𝕄 = ⟨Ψ|M|Ψ'⟩
        M_psi_prime = mirror_op.M @ psi_prime
        mirror_constant = np.vdot(psi, M_psi_prime)
        
        return mirror_constant
    
    @staticmethod
    def coherence_measure(mirror_constant: complex) -> float:
        """
        Measure quantum coherence from mirror constant.
        Perfect coherence: |𝕄| = 1
        
        Returns:
            Coherence value between 0 and 1
        """
        return abs(mirror_constant)
    
    @staticmethod
    def verify_identity(observer_state: QuantumState,
                       reflection_state: QuantumState,
                       mirror_op: MirrorOperator,
                       tolerance: float = 1e-10) -> Tuple[bool, float]:
        """
        Verify the mirror equation: |Ψ⟩ ≡ M|Ψ'⟩
        
        Returns:
            (is_identical, deviation)
        """
        psi = observer_state.get_state_vector()
        psi_prime = reflection_state.get_state_vector()
        
        if psi is None or psi_prime is None:
            raise ValueError("States must be pure for identity verification")
        
        M_psi_prime = mirror_op.M @ psi_prime
        
        # Check if |Ψ⟩ = M|Ψ'⟩ up to global phase
        # Calculate overlap
        overlap = np.vdot(psi, M_psi_prime)
        deviation = 1.0 - abs(overlap)
        
        is_identical = deviation < tolerance
        
        return is_identical, deviation


class QuantumMirrorSystem:
    """
    Complete Quantum Mirror Theory system integrating all components.
    """
    
    def __init__(self, dimension: int, operator_type: str = 'reflection'):
        """
        Initialize quantum mirror system.
        
        Args:
            dimension: Hilbert space dimension
            operator_type: Type of mirror operator
        """
        self.dimension = dimension
        self.mirror_operator = MirrorOperator(dimension, operator_type)
        self.observer_state = None
        self.reflection_state = None
    
    def set_observer_state(self, state: Union[np.ndarray, QuantumState]):
        """Set the observer state |Ψ⟩"""
        if isinstance(state, np.ndarray):
            self.observer_state = QuantumState(state)
        else:
            self.observer_state = state
    
    def generate_reflection_state(self) -> QuantumState:
        """
        Generate reflection state |Ψ'⟩ from observer state.
        For perfect mirror: |Ψ'⟩ = M|Ψ⟩
        """
        if self.observer_state is None:
            raise ValueError("Observer state not set")
        
        self.reflection_state = self.mirror_operator.apply(self.observer_state)
        return self.reflection_state
    
    def calculate_mirror_constant(self) -> complex:
        """Calculate the Mirror Constant for current states"""
        if self.observer_state is None or self.reflection_state is None:
            raise ValueError("Both observer and reflection states must be set")
        
        return MirrorConstant.calculate(
            self.observer_state,
            self.reflection_state,
            self.mirror_operator
        )
    
    def verify_mirror_equation(self, tolerance: float = 1e-10) -> dict:
        """
        Comprehensive verification of mirror equation.
        
        Returns:
            Dictionary with verification results
        """
        if self.observer_state is None:
            raise ValueError("Observer state not set")
        
        # Generate reflection state
        self.generate_reflection_state()
        
        # Calculate mirror constant
        M_value = self.calculate_mirror_constant()
        coherence = MirrorConstant.coherence_measure(M_value)
        
        # Verify identity
        is_identical, deviation = MirrorConstant.verify_identity(
            self.observer_state,
            self.reflection_state,
            self.mirror_operator,
            tolerance
        )
        
        # Check operator properties
        eigenvalues, _ = self.mirror_operator.eigendecomposition()
        
        results = {
            'mirror_constant': M_value,
            'coherence': coherence,
            'is_perfect_mirror': is_identical,
            'deviation': deviation,
            'operator_eigenvalues': eigenvalues,
            'state_purity': self.observer_state.purity(),
            'dimension': self.dimension
        }
        
        return results
    
    def time_evolution(self, 
                      hamiltonian: np.ndarray, 
                      time: float,
                      steps: int = 100) -> dict:
        """
        Evolve system under Hamiltonian and track mirror properties.
        
        Args:
            hamiltonian: System Hamiltonian
            time: Total evolution time
            steps: Number of time steps
            
        Returns:
            Dictionary with evolution data
        """
        if self.observer_state is None:
            raise ValueError("Observer state not set")
        
        # Verify [M, H] = 0 for conservation
        commutator = self.mirror_operator.commutator_with(hamiltonian)
        commutator_norm = np.linalg.norm(commutator)
        
        dt = time / steps
        times = np.linspace(0, time, steps)
        
        # Time evolution operator
        U = expm(-1j * hamiltonian * dt)
        
        mirror_constants = []
        coherences = []
        purities = []
        
        current_state = self.observer_state.get_state_vector().copy()
        
        for t in times:
            # Set current observer state
            self.set_observer_state(current_state)
            
            # Generate reflection
            self.generate_reflection_state()
            
            # Calculate properties
            M_value = self.calculate_mirror_constant()
            mirror_constants.append(M_value)
            coherences.append(abs(M_value))
            purities.append(self.observer_state.purity())
            
            # Evolve state
            current_state = U @ current_state
        
        return {
            'times': times,
            'mirror_constants': np.array(mirror_constants),
            'coherences': np.array(coherences),
            'purities': np.array(purities),
            'commutator_norm': commutator_norm,
            'is_conserved': commutator_norm < 1e-10
        }


def create_qudit_state(dimension: int, 
                       state_type: str = 'superposition') -> QuantumState:
    """
    Create various qudit states for testing.
    
    Args:
        dimension: Qudit dimension
        state_type: Type of state to create
            - 'ground': Ground state |0⟩
            - 'excited': Maximally excited state
            - 'superposition': Equal superposition
            - 'random': Random pure state
            - 'coherent': Coherent state
    
    Returns:
        QuantumState object
    """
    if state_type == 'ground':
        state = np.zeros(dimension, dtype=complex)
        state[0] = 1.0
    
    elif state_type == 'excited':
        state = np.zeros(dimension, dtype=complex)
        state[-1] = 1.0
    
    elif state_type == 'superposition':
        state = np.ones(dimension, dtype=complex) / np.sqrt(dimension)
    
    elif state_type == 'random':
        # Random normalized state
        real_part = np.random.randn(dimension)
        imag_part = np.random.randn(dimension)
        state = real_part + 1j * imag_part
        state = state / np.linalg.norm(state)
    
    elif state_type == 'coherent':
        # Coherent state with varying phases
        state = np.array([np.exp(1j * 2 * np.pi * k / dimension) 
                         for k in range(dimension)], dtype=complex)
        state = state / np.sqrt(dimension)
    
    else:
        raise ValueError(f"Unknown state type: {state_type}")
    
    return QuantumState(state)


def harmonic_oscillator_hamiltonian(dimension: int, omega: float = 1.0) -> np.ndarray:
    """
    Create harmonic oscillator Hamiltonian in truncated basis.
    H = ω(a†a + 1/2)
    
    Args:
        dimension: Number of levels
        omega: Angular frequency
        
    Returns:
        Hamiltonian matrix
    """
    H = np.diag([omega * (n + 0.5) for n in range(dimension)])
    return H


def spin_hamiltonian(dimension: int, coupling: float = 1.0) -> np.ndarray:
    """
    Create spin Hamiltonian for qudit.
    
    Args:
        dimension: Spin dimension
        coupling: Coupling strength
        
    Returns:
        Hamiltonian matrix
    """
    # Generalized Pauli matrices for qudits
    H = np.zeros((dimension, dimension), dtype=complex)
    
    for i in range(dimension - 1):
        H[i, i+1] = coupling
        H[i+1, i] = coupling
    
    return H
