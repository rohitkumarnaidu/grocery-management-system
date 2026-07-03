import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Store, ShoppingCart, Package, Plus, Trash2, Sparkles, Clock, Receipt, Search, ChevronRight, Leaf } from 'lucide-react';
import UiverseButton from '@/components/UiverseButton';

const API_URL = 'http://127.0.0.1:5000/api';

const CATEGORIES = [
  'Dairy', 'Beverages', 'Snacks', 'Fruits and Vegetables',
  'Grains and Cereals', 'Bakery', 'Meat and Seafood',
  'Frozen Foods', 'Household', 'Other'
];

const CATEGORY_EMOJI = {
  'Dairy': '🥛', 'Beverages': '🧃', 'Snacks': '🍿',
  'Fruits and Vegetables': '🥬', 'Grains and Cereals': '🌾',
  'Bakery': '🥖', 'Meat and Seafood': '🥩',
  'Frozen Foods': '🧊', 'Household': '🏠', 'Other': '📦'
};

export default function App() {
  const [view, setView] = useState('customer');
  const [inventory, setInventory] = useState({});
  const [cart, setCart] = useState({});
  const [totalPrice, setTotalPrice] = useState(0);
  const [orders, setOrders] = useState([]);

  const [newItem, setNewItem] = useState('');
  const [newPrice, setNewPrice] = useState('');
  const [newQty, setNewQty] = useState('');
  const [newCategory, setNewCategory] = useState('Other');

  const [selectedCategory, setSelectedCategory] = useState('All');
  const [adminCategoryFilter, setAdminCategoryFilter] = useState('All');
  const [checkoutSuccess, setCheckoutSuccess] = useState(false);

  const loadData = async () => {
    try {
      const prodRes = await fetch(`${API_URL}/products`);
      if (prodRes.ok) setInventory(await prodRes.json());
      
      const cartRes = await fetch(`${API_URL}/cart`);
      if (cartRes.ok) {
        const data = await cartRes.json();
        setCart(data.cart);
        setTotalPrice(data.total_price);
      }

      const ordersRes = await fetch(`${API_URL}/orders`);
      if (ordersRes.ok) setOrders(await ordersRes.json());
    } catch (e) {
      console.error('API Error:', e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const addToCart = async (item) => {
    await fetch(`${API_URL}/cart`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item, qty: 1 })
    });
    loadData();
  };

  const updateCartQty = async (item, qty) => {
    await fetch(`${API_URL}/cart/${item}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ qty: parseInt(qty) })
    });
    loadData();
  };

  const removeFromCart = async (item) => {
    await fetch(`${API_URL}/cart/${item}`, { method: 'DELETE' });
    loadData();
  };

  const handleCheckout = async () => {
    const res = await fetch(`${API_URL}/checkout`, { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      setCheckoutSuccess(true);
      setTimeout(() => setCheckoutSuccess(false), 3000);
      loadData();
    } else {
      alert(data.message);
    }
  };

  const addProduct = async (e) => {
    e.preventDefault();
    await fetch(`${API_URL}/products`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item: newItem, price: parseFloat(newPrice), qty: parseInt(newQty), category: newCategory })
    });
    setNewItem(''); setNewPrice(''); setNewQty(''); setNewCategory('Other');
    loadData();
  };

  const updateProductPrice = async (item, price) => {
    await fetch(`${API_URL}/products/${item}/price`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ price: parseFloat(price) })
    });
    loadData();
  };

  const updateProductQty = async (item, qty) => {
    await fetch(`${API_URL}/products/${item}/qty`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ qty: parseInt(qty) })
    });
    loadData();
  };

  const deleteProduct = async (item) => {
    await fetch(`${API_URL}/products/${item}`, { method: 'DELETE' });
    loadData();
  };

  const cartItemCount = Object.values(cart).reduce((sum, [, qty]) => sum + qty, 0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-violet-50/30 text-slate-800 flex flex-col items-center overflow-x-hidden font-sans selection:bg-violet-200 relative">
      
      {/* Decorative background elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
        <div className="absolute top-[-15%] right-[-10%] w-[600px] h-[600px] bg-violet-200/30 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-15%] left-[-10%] w-[500px] h-[500px] bg-blue-100/40 rounded-full blur-[120px]"></div>
        <div className="absolute top-[50%] left-[50%] w-[400px] h-[400px] bg-amber-100/20 rounded-full blur-[100px]"></div>
      </div>
      
      {/* Checkout success toast */}
      {checkoutSuccess && (
        <div className="fixed top-6 right-6 z-50 bg-emerald-500 text-white px-6 py-4 rounded-2xl shadow-lg shadow-emerald-500/20 flex items-center gap-3 animate-bounce">
          <span className="text-xl">✓</span>
          <span className="font-semibold">Order placed successfully!</span>
        </div>
      )}
      
      <div className="w-full max-w-7xl p-4 sm:p-6 lg:p-8 relative z-10">
        
        {/* Header */}
        <header className="flex flex-col md:flex-row justify-between items-center py-5 px-8 mb-8 bg-white/70 border border-slate-200/60 backdrop-blur-xl rounded-2xl shadow-sm gap-5">
          <div className="text-2xl font-bold bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-violet-500 to-purple-600 rounded-xl flex items-center justify-center shadow-md shadow-violet-500/20">
              <Leaf className="w-5 h-5 text-white" strokeWidth={2.5} />
            </div>
            Stock Smart
          </div>
          <nav className="flex gap-1.5 p-1.5 bg-slate-100/80 rounded-full border border-slate-200/50">
            <button 
              className={`px-6 py-2.5 rounded-full text-sm font-semibold transition-all duration-300 ${view === 'customer' ? 'bg-white text-violet-700 shadow-md shadow-slate-200/50' : 'text-slate-500 hover:text-slate-700 hover:bg-white/50'}`}
              onClick={() => setView('customer')}>
              🛒 Shop
            </button>
            <button 
              className={`px-6 py-2.5 rounded-full text-sm font-semibold transition-all duration-300 ${view === 'admin' ? 'bg-white text-violet-700 shadow-md shadow-slate-200/50' : 'text-slate-500 hover:text-slate-700 hover:bg-white/50'}`}
              onClick={() => setView('admin')}>
              📊 Dashboard
            </button>
          </nav>
        </header>

        {view === 'customer' && (
          <>
            {/* Category Filter Pills */}
            <div className="mb-8 flex flex-wrap gap-2.5 justify-center max-w-5xl mx-auto">
              <button 
                className={`px-5 py-2.5 rounded-full text-sm font-medium transition-all duration-300 border ${selectedCategory === 'All' ? 'bg-violet-600 border-violet-600 text-white shadow-md shadow-violet-600/20' : 'bg-white border-slate-200 text-slate-600 hover:bg-violet-50 hover:text-violet-700 hover:border-violet-200 shadow-sm'}`}
                onClick={() => setSelectedCategory('All')}>
                ✨ All
              </button>
              {CATEGORIES.map(cat => (
                <button 
                  key={cat} 
                  className={`px-5 py-2.5 rounded-full text-sm font-medium transition-all duration-300 border ${selectedCategory === cat ? 'bg-violet-600 border-violet-600 text-white shadow-md shadow-violet-600/20' : 'bg-white border-slate-200 text-slate-600 hover:bg-violet-50 hover:text-violet-700 hover:border-violet-200 shadow-sm'}`}
                  onClick={() => setSelectedCategory(cat)}>
                  {CATEGORY_EMOJI[cat]} {cat}
                </button>
              ))}
            </div>

            <div className="grid lg:grid-cols-3 gap-8">
              {/* Product Grid Panel */}
              <div className="lg:col-span-2 bg-white/60 border border-slate-200/50 backdrop-blur-xl rounded-3xl p-8 shadow-sm">
                <div className="flex items-center justify-between mb-8">
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 bg-violet-100 rounded-xl">
                      <Store className="w-5 h-5 text-violet-600" />
                    </div>
                    <h2 className="text-xl font-bold text-slate-800 tracking-tight">Fresh Products</h2>
                  </div>
                  <span className="text-sm text-slate-400 font-medium">
                    {Object.keys(inventory).filter(item => {
                      const [, , category = 'Other'] = inventory[item];
                      return selectedCategory === 'All' || category === selectedCategory;
                    }).length} items
                  </span>
                </div>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
                  {Object.keys(inventory).length === 0 ? (
                     <div className="col-span-full text-center text-slate-400 py-16 flex flex-col items-center gap-4">
                       <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center">
                         <Sparkles className="w-7 h-7 text-slate-300" />
                       </div>
                       <p className="font-medium">No products available yet</p>
                       <p className="text-sm text-slate-400">Check back soon!</p>
                     </div>
                  ) : (
                    Object.keys(inventory).filter(item => {
                      const [, , category = 'Other'] = inventory[item];
                      return selectedCategory === 'All' || category === selectedCategory;
                    }).map(item => {
                      const [price, qty, category = 'Other'] = inventory[item];
                      return (
                        <div key={item} className="group relative border border-slate-200/60 rounded-2xl p-5 bg-white hover:border-violet-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-violet-100/50 transition-all duration-400">
                          
                          <div className="text-3xl mb-4 flex justify-center">
                            {CATEGORY_EMOJI[category] || '📦'}
                          </div>
                          <div className="font-bold text-slate-800 capitalize text-base mb-0.5 text-center">{item}</div>
                          <div className="text-[11px] font-semibold uppercase tracking-wider text-violet-500 mb-4 text-center">{category}</div>
                          
                          <div className="flex items-end justify-center gap-0.5 mb-4">
                            <span className="text-sm text-slate-400 mb-0.5 font-medium">$</span>
                            <span className="text-2xl font-extrabold text-slate-800">{price}</span>
                          </div>
                          
                          <div className="flex justify-between items-center text-xs text-slate-500 mb-5 bg-slate-50 px-3.5 py-2 rounded-xl border border-slate-100">
                            <span className="font-medium">In Stock</span>
                            <span className={qty > 0 ? "text-emerald-600 font-bold" : "text-red-500 font-bold"}>{qty > 0 ? `${qty} units` : 'Sold Out'}</span>
                          </div>

                          <UiverseButton className="w-full text-sm font-semibold h-11" disabled={qty === 0} onClick={() => addToCart(item)}>
                            <Plus className="w-4 h-4 mr-1.5"/> Add to Cart
                          </UiverseButton>
                        </div>
                      )
                    })
                  )}
                </div>
              </div>
              
              {/* Cart Panel */}
              <div>
                <div className="sticky top-6 bg-white/60 border border-slate-200/50 backdrop-blur-xl rounded-3xl p-7 shadow-sm">
                  <div className="flex items-center justify-between mb-7">
                    <div className="flex items-center gap-3">
                      <div className="p-2.5 bg-amber-100 rounded-xl">
                        <ShoppingCart className="w-5 h-5 text-amber-600" />
                      </div>
                      <h2 className="text-xl font-bold text-slate-800 tracking-tight">Cart</h2>
                    </div>
                    {cartItemCount > 0 && (
                      <span className="bg-violet-600 text-white text-xs font-bold px-2.5 py-1 rounded-full">{cartItemCount}</span>
                    )}
                  </div>
                  
                  <div className="max-h-[420px] overflow-y-auto pr-1 flex flex-col gap-3 mb-6 custom-scrollbar">
                    {Object.keys(cart).length === 0 ? (
                      <div className="text-slate-400 text-sm text-center py-10 flex flex-col items-center gap-3">
                        <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center text-2xl">🛒</div>
                        <p>Your cart is empty</p>
                      </div>
                    ) : (
                      Object.keys(cart).map(item => {
                        const [price, qty] = cart[item];
                        return (
                          <div key={item} className="flex justify-between items-center p-3.5 rounded-xl bg-slate-50 border border-slate-100 hover:border-slate-200 transition-colors group">
                            <div>
                              <div className="font-semibold text-slate-700 capitalize text-sm">{item}</div>
                              <div className="text-xs font-medium text-slate-400 mt-0.5">${price} <span className="text-slate-300 mx-0.5">×</span> {qty} = <span className="text-violet-600 font-semibold">${(price * qty).toFixed(2)}</span></div>
                            </div>
                            <div className="flex items-center gap-2">
                              <Input 
                                type="number" 
                                className="w-14 h-8 bg-white border-slate-200 text-slate-700 text-sm px-2 text-center rounded-lg focus:border-violet-400 focus:ring-1 focus:ring-violet-400" 
                                value={qty} 
                                onChange={(e) => updateCartQty(item, e.target.value)}
                                min="0"
                              />
                              <button className="text-slate-400 hover:text-red-500 p-1.5 rounded-lg hover:bg-red-50 transition-colors" onClick={() => removeFromCart(item)}>
                                <Trash2 className="w-3.5 h-3.5" />
                              </button>
                            </div>
                          </div>
                        )
                      })
                    )}
                  </div>
                  
                  <div className="p-4 rounded-2xl bg-gradient-to-r from-violet-50 to-purple-50 border border-violet-100 flex justify-between items-center text-sm font-semibold text-slate-700 mb-5">
                    <span>Total</span>
                    <span className="text-xl font-extrabold text-violet-700">${totalPrice.toFixed(2)}</span>
                  </div>
                  
                  <UiverseButton className="w-full text-sm font-semibold h-12" disabled={Object.keys(cart).length === 0} onClick={handleCheckout}>
                    Checkout <ChevronRight className="w-4 h-4 ml-1" />
                  </UiverseButton>
                </div>
              </div>
            </div>

            {/* Customer Order History */}
            {orders.length > 0 && (
              <div className="mt-8 bg-white/60 border border-slate-200/50 backdrop-blur-xl rounded-3xl p-8 shadow-sm">
                <div className="flex items-center gap-3 mb-7">
                  <div className="p-2.5 bg-emerald-100 rounded-xl">
                    <Clock className="w-5 h-5 text-emerald-600" />
                  </div>
                  <h2 className="text-xl font-bold text-slate-800 tracking-tight">Recent Orders</h2>
                </div>
                
                <div className="space-y-3">
                  {orders.map((order, i) => (
                    <div key={i} className="p-5 rounded-2xl bg-slate-50 border border-slate-100 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 hover:border-slate-200 transition-colors">
                      <div>
                        <div className="font-bold text-slate-700 mb-0.5 flex items-center gap-2">
                          <span className="text-violet-600">#{order.id}</span>
                        </div>
                        <div className="text-xs text-slate-400 font-medium">{order.timestamp}</div>
                      </div>
                      <div className="flex-1 max-w-md">
                        <div className="text-sm text-slate-500 leading-relaxed">
                          {order.items.map(item => `${item.qty}× ${item.item}`).join(' · ')}
                        </div>
                      </div>
                      <div className="text-emerald-600 font-extrabold text-lg bg-emerald-50 px-4 py-2 rounded-xl border border-emerald-100">
                        ${order.total.toFixed(2)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        {view === 'admin' && (
          <div className="max-w-5xl mx-auto space-y-8">
            
            {/* Add Product Panel */}
            <div className="bg-white/60 border border-slate-200/50 backdrop-blur-xl rounded-3xl p-8 shadow-sm">
              <div className="flex items-center gap-3 mb-7">
                <div className="p-2.5 bg-violet-100 rounded-xl">
                  <Plus className="w-5 h-5 text-violet-600" />
                </div>
                <h2 className="text-xl font-bold text-slate-800 tracking-tight">Add New Product</h2>
              </div>
              
              <form onSubmit={addProduct} className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4">
                <Input placeholder="Product name" className="md:col-span-1 bg-white border-slate-200 text-slate-700 h-12 rounded-xl focus:border-violet-400 focus:ring-1 focus:ring-violet-400 placeholder:text-slate-400" value={newItem} onChange={e => setNewItem(e.target.value)} required />
                <Input type="number" step="0.01" min="0" placeholder="Price ($)" className="md:col-span-1 bg-white border-slate-200 text-slate-700 h-12 rounded-xl focus:border-violet-400 focus:ring-1 focus:ring-violet-400 placeholder:text-slate-400" value={newPrice} onChange={e => setNewPrice(e.target.value)} required />
                <Input type="number" min="1" placeholder="Stock qty" className="md:col-span-1 bg-white border-slate-200 text-slate-700 h-12 rounded-xl focus:border-violet-400 focus:ring-1 focus:ring-violet-400 placeholder:text-slate-400" value={newQty} onChange={e => setNewQty(e.target.value)} required />
                <select className="md:col-span-1 bg-white border-slate-200 text-slate-700 rounded-xl px-4 border text-sm h-12 focus:outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-400" value={newCategory} onChange={e => setNewCategory(e.target.value)}>
                  {CATEGORIES.map(cat => <option key={cat} value={cat}>{CATEGORY_EMOJI[cat]} {cat}</option>)}
                </select>
                <UiverseButton type="submit" className="md:col-span-1 h-12 text-sm font-semibold rounded-xl">Add Product</UiverseButton>
              </form>
            </div>

            {/* Inventory Panel */}
            <div className="bg-white/60 border border-slate-200/50 backdrop-blur-xl rounded-3xl p-8 shadow-sm">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-5 mb-7">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 bg-blue-100 rounded-xl">
                    <Package className="w-5 h-5 text-blue-600" />
                  </div>
                  <h2 className="text-xl font-bold text-slate-800 tracking-tight">Inventory</h2>
                </div>
                
                <div className="flex items-center gap-2 bg-slate-50 p-1.5 rounded-xl border border-slate-200">
                  <Search className="w-4 h-4 text-slate-400 ml-2" />
                  <select className="bg-transparent border-0 text-slate-600 rounded-lg px-2 py-1.5 text-sm font-medium focus:outline-none focus:ring-0 cursor-pointer" value={adminCategoryFilter} onChange={e => setAdminCategoryFilter(e.target.value)}>
                    <option value="All">All Categories</option>
                    {CATEGORIES.map(cat => <option key={cat} value={cat}>{cat}</option>)}
                  </select>
                </div>
              </div>

              <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white">
                <Table>
                  <TableHeader>
                    <TableRow className="border-slate-100 hover:bg-transparent bg-slate-50">
                      <TableHead className="text-slate-500 font-semibold h-12 px-6 text-xs uppercase tracking-wider">Product</TableHead>
                      <TableHead className="text-slate-500 font-semibold h-12 text-xs uppercase tracking-wider">Category</TableHead>
                      <TableHead className="text-slate-500 font-semibold text-right h-12 text-xs uppercase tracking-wider">Price</TableHead>
                      <TableHead className="text-slate-500 font-semibold text-right h-12 text-xs uppercase tracking-wider">Stock</TableHead>
                      <TableHead className="h-12 w-12"></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {Object.keys(inventory).filter(item => {
                      const [, , category = 'Other'] = inventory[item];
                      return adminCategoryFilter === 'All' || category === adminCategoryFilter;
                    }).length === 0 ? (
                      <TableRow className="border-0">
                        <TableCell colSpan={5} className="text-center py-16 text-slate-400">
                          <div className="flex flex-col items-center gap-3">
                            <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center">
                              <Sparkles className="w-5 h-5 text-slate-300" />
                            </div>
                            <span className="font-medium">No products match this filter</span>
                          </div>
                        </TableCell>
                      </TableRow>
                    ) : (
                      Object.keys(inventory).filter(item => {
                        const [, , category = 'Other'] = inventory[item];
                        return adminCategoryFilter === 'All' || category === adminCategoryFilter;
                      }).map(item => {
                        const [price, qty, category = 'Other'] = inventory[item];
                        return (
                          <TableRow key={item} className="border-slate-100 hover:bg-violet-50/30 transition-colors group">
                            <TableCell className="capitalize font-semibold text-slate-700 px-6 py-4">
                              <span className="mr-2">{CATEGORY_EMOJI[category] || '📦'}</span>
                              {item}
                            </TableCell>
                            <TableCell>
                              <span className="px-3 py-1 rounded-full bg-violet-50 border border-violet-100 text-violet-600 text-[11px] font-bold tracking-wider uppercase">
                                {category}
                              </span>
                            </TableCell>
                            <TableCell className="text-right py-4">
                              <div className="flex items-center justify-end gap-1.5">
                                <span className="text-slate-400 text-sm">$</span>
                                <Input type="number" step="0.01" className="w-24 h-9 bg-slate-50 border-slate-200 text-slate-700 text-right px-3 rounded-lg focus:border-violet-400 focus:ring-1 focus:ring-violet-400" defaultValue={price} onBlur={(e) => updateProductPrice(item, e.target.value)} />
                              </div>
                            </TableCell>
                            <TableCell className="text-right py-4">
                              <Input type="number" className="w-20 ml-auto h-9 bg-slate-50 border-slate-200 text-slate-700 text-right px-3 rounded-lg focus:border-violet-400 focus:ring-1 focus:ring-violet-400" defaultValue={qty} onBlur={(e) => updateProductQty(item, e.target.value)} />
                            </TableCell>
                            <TableCell className="text-right px-4 py-4">
                              <button className="text-slate-300 hover:text-red-500 p-2 rounded-xl hover:bg-red-50 transition-all opacity-0 group-hover:opacity-100 focus:opacity-100" onClick={() => deleteProduct(item)} title="Delete">
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </TableCell>
                          </TableRow>
                        )
                      })
                    )}
                  </TableBody>
                </Table>
              </div>
            </div>

            {/* Admin Order History Panel */}
            <div className="bg-white/60 border border-slate-200/50 backdrop-blur-xl rounded-3xl p-8 shadow-sm">
              <div className="flex items-center gap-3 mb-7">
                <div className="p-2.5 bg-emerald-100 rounded-xl">
                  <Receipt className="w-5 h-5 text-emerald-600" />
                </div>
                <h2 className="text-xl font-bold text-slate-800 tracking-tight">Order Ledger</h2>
              </div>

              <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white">
                <Table>
                  <TableHeader>
                    <TableRow className="border-slate-100 hover:bg-transparent bg-slate-50">
                      <TableHead className="text-slate-500 font-semibold h-12 px-6 text-xs uppercase tracking-wider">Order ID</TableHead>
                      <TableHead className="text-slate-500 font-semibold h-12 text-xs uppercase tracking-wider">Date & Time</TableHead>
                      <TableHead className="text-slate-500 font-semibold h-12 text-xs uppercase tracking-wider">Items</TableHead>
                      <TableHead className="text-slate-500 font-semibold text-right h-12 pr-6 text-xs uppercase tracking-wider">Total</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {orders.length === 0 ? (
                      <TableRow className="border-0">
                        <TableCell colSpan={4} className="text-center py-14 text-slate-400 font-medium">No orders yet</TableCell>
                      </TableRow>
                    ) : (
                      orders.map((order, i) => (
                        <TableRow key={i} className="border-slate-100 hover:bg-emerald-50/30 transition-colors">
                          <TableCell className="font-bold text-violet-600 px-6 py-4">#{order.id}</TableCell>
                          <TableCell className="text-slate-500 text-sm">{order.timestamp}</TableCell>
                          <TableCell className="text-slate-500 text-sm max-w-xs">
                            {order.items.map(item => `${item.qty}× ${item.item}`).join(' · ')}
                          </TableCell>
                          <TableCell className="text-right pr-6 py-4 font-bold text-emerald-600">
                            ${order.total.toFixed(2)}
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </div>
            </div>

          </div>
        )}
      </div>
      
      {/* Scrollbar styling */}
      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 5px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(0, 0, 0, 0.08);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(0, 0, 0, 0.15);
        }
      `}</style>
    </div>
  );
}
